import numpy as np
import pickle
import os

import matplotlib.pyplot as plt
import collections

import torch
import torch.nn as nn
import torch.nn.functional as F

from baselines.swag.swag_utils import bn_update, predict
from baselines.swag import swag


def set_seed(RANDOM_SEED=0):
    '''
    Set seed for reproduction
    '''
    torch.manual_seed(RANDOM_SEED)
    np.random.seed(RANDOM_SEED)
    torch.cuda.manual_seed(RANDOM_SEED)
    torch.cuda.manual_seed_all(RANDOM_SEED) # if use multi-GPU
    torch.backends.cudnn.deterministic = True
    torch.backends.cudnn.benchmark = False
    import random
    random.seed(RANDOM_SEED)


def load_pkl_data(data_path):
    '''
    Load toy data saving as pickle file
    '''
    with open(data_path,'rb') as f:
        tr_dat, down_dat, val_dat, te_dat  = pickle.load(f)
    return tr_dat, down_dat, val_dat, te_dat


# save model
def save_checkpoint(file_path, epoch, **kwargs):
    state = {"epoch": epoch}
    state.update(kwargs)
    torch.save(state, file_path)


# parameter list to state_dict(ordered Dict)
def list_to_state_dict(model, sample_list):
    ordDict = collections.OrderedDict()
    for sample, (name, param) in zip(sample_list, model.named_parameters()):
        ordDict[name] = sample
    return ordDict


def unflatten_like_size(vector, likeTensorSize):
    # Takes a flat torch.tensor and unflattens it to a list of torch.tensors
    # Input
    #  - vector : flattened parameters
    #  - likeTensorSize : list of torch.Size
    outList = []
    i = 0
    for layer_size in likeTensorSize:
        n = layer_size.numel()
        outList.append(vector[i : i + n].view(layer_size))
        i += n

    return outList


# NLL
# https://github.com/wjmaddox/swa_gaussian/blob/master/experiments/uncertainty/uncertainty.py#L78
def nll(outputs, labels):
    labels = labels.astype(int)
    idx = (np.arange(labels.size), labels)
    ps = outputs[idx]
    nll = -np.sum(np.log(ps))
    return nll


class StepLR:
    def __init__(self, optimizer, learning_rate: float, total_epochs: int):
        self.optimizer = optimizer
        self.total_epochs = total_epochs
        self.base = learning_rate

    def __call__(self, epoch):
        if epoch < self.total_epochs * 3/10:
            lr = self.base
        elif epoch < self.total_epochs * 6/10:
            lr = self.base * 0.2
        elif epoch < self.total_epochs * 8/10:
            lr = self.base * 0.2 ** 2
        else:
            lr = self.base * 0.2 ** 3

        for param_group in self.optimizer.param_groups:
            param_group["lr"] = lr

    def lr(self) -> float:
        return self.optimizer.param_groups[0]["lr"]



# deactivate batchnorm
# https://discuss.pytorch.org/t/how-to-close-batchnorm-when-using-torchvision-models/21812
def deactivate_batchnorm(m):
    if isinstance(m, nn.BatchNorm2d):
        m.reset_parameters()
        m.eval()
        with torch.no_grad():
            m.weight.fill_(1.0)
            m.bias.zero_()



# train SGD
def train_sgd(dataloader, model, criterion, optimizer, device, batch_norm=True):
    loss_sum = 0.0
    correct = 0.0

    num_objects_current = 0
    num_batches = len(dataloader)

    model.train()
    if batch_norm == False:
        model.apply(deactivate_batchnorm)
        print("Deactivate batch normalization layers")

    for batch, (inputs, targets) in enumerate(dataloader):
        inputs, targets = inputs.to(device), targets.to(device)

        pred = model(inputs)
        loss = criterion(pred, targets)
        correct += (pred.argmax(1) == targets).type(torch.float).sum().item()
        
        # Backprop
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
        
        loss_sum += loss.data.item() * inputs.size(0)
        num_objects_current += inputs.size(0)
    return {
        "loss": loss_sum / num_objects_current,
        "accuracy": correct / num_objects_current * 100.0,
    }


# train SAM, FSAM
def train_sam(dataloader, model, criterion, optimizer, device, batch_norm=True):
    loss_sum = 0.0
    correct = 0.0

    num_objects_current = 0
    num_batches = len(dataloader)

    model.train()
    if batch_norm == False:
        model.apply(deactivate_batchnorm)
        print("Deactivate batch normalization layers")

    for batch, (X, y) in enumerate(dataloader):
        X, y = X.to(device), y.to(device)
        # pred = model(X)

        # first forward-backward pass
        loss = criterion(model(X), y)
        loss.backward()
        optimizer.first_step(zero_grad=True)

        # second forward-backward pass
        criterion(model(X), y).backward()
        optimizer.second_step(zero_grad=True)

        correct += (model(X).argmax(1) == y).type(torch.float).sum().item()
        loss_sum += loss.data.item() * X.size(0)
        num_objects_current += X.size(0)
    return {
        "loss": loss_sum / num_objects_current,
        "accuracy": correct / num_objects_current * 100.0,
    }


# train BSAM
def train_bsam(dataloader, sabtl_model, criterion, optimizer, device, batch_norm=True):
    loss_sum = 0.0
    correct = 0.0

    num_objects_current = 0
    num_batches = len(dataloader)

    sabtl_model.backbone.train()
    
    # Set weight sample
    sample_w, z_1, z_2 = sabtl_model.sample()

    # Set Sampled weight to DNN model
    sabtl_model.set_sampled_parameters(sample_w)
    
    if batch_norm == False:
        sabtl_model.backbone.apply(deactivate_batchnorm)
        print("Deactivate batch normalization layers")

    for batch, (X, y) in enumerate(dataloader):
        X, y = X.to(device), y.to(device)

        # Making matrix A
        if sabtl_model.diag_only:
            '''
            sparse matrix???
            1. I_p
            2. diag( z_1~z_p )
            ?????????
            stack
            '''
        else:
            raise "Not implemented yet"

        # first forward-backward pass
        # pred = sabtl_model.backbone(X)
        loss = criterion(sabtl_model.backbone(X), y)
        loss.backward()
        optimizer.first_step(zero_grad=True)

        # second forward-backward pass
        # pred = sabtl_model.backbone(X)
        criterion(sabtl_model.backbone(X), y).backward()
        optimizer.second_step(zero_grad=True)

        correct += (sabtl_model.backbone(X).argmax(1) == y).type(torch.float).sum().item()
        loss_sum += loss.data.item() * X.size(0)
        num_objects_current += X.size(0)
        
    return {
        "loss": loss_sum / num_objects_current,
        "accuracy": correct / num_objects_current * 100.0,
    }


# Test
def eval(loader, model, criterion, device):
    loss_sum = 0.0
    correct = 0.0
    num_objects_total = len(loader.dataset)

    model.eval()
    
    with torch.no_grad():
        for i, (inputs, targets) in enumerate(loader):
            inputs, targets = inputs.to(device), targets.to(device)
            pred = model(inputs)
            loss = criterion(pred, targets)
            loss_sum += loss.item() * inputs.size(0)
            correct += (pred.argmax(1) == targets).type(torch.float).sum().item()

    return {
        "loss": loss_sum / num_objects_total,
        "accuracy": correct / num_objects_total * 100.0,
    }



def eval_metrics(loader, model, criterion, device, num_bins=50, eps=1e-8):
    '''
    get loss, accuracy, nll and ece for every eval step
    '''
    loss_sum = 0.0
    num_objects_total = len(loader.dataset)

    preds = list()
    targets = list()

    model.eval()
    offset = 0
    with torch.no_grad():
        for _, (input, target) in enumerate(loader):
            input, target = input.to(device), target.to(device)
            pred = model(input)
            loss = criterion(pred, target)
            loss_sum += loss.item() * input.size(0)
            
            preds.append(F.softmax(pred, dim=1).cpu().numpy())
            targets.append(target.cpu().numpy())
            offset += input.size(0)
    
    preds = np.vstack(preds)
    targets = np.concatenate(targets)

    accuracy = np.mean(np.argmax(preds, axis=1) == targets)
    nll = -np.mean(np.log(preds[np.arange(preds.shape[0]), targets] + eps))
    ece = calibration_curve(preds, targets, num_bins)['ece']
    
    return {
        "loss" : loss_sum / num_objects_total,
        "accuracy" : accuracy * 100.0,
        "nll" : nll,
        "ece" : ece,
    }


def bma(tr_loader, te_loader, model, bma_num_models, num_classes, bma_save_path=None, eps=1e-8, batch_norm=True):
    '''
    run bayesian model averaging in test step
    '''
    # Save mean weight of model as number 0
    if bma_save_path is not None:
        sample = model.sample(0)
        torch.save(sample, f'{bma_save_path}/bma_model-0.pt')


    swag_predictions = np.zeros((len(te_loader.dataset), num_classes))
    with torch.no_grad():
        for i in range(bma_num_models):

            sample = model.sample(1.0, cov=True)
            
            # print("SWAG Sample %d/%d. BN update" % (i + 1, bma_num_models))
            if batch_norm:
                bn_update(tr_loader, model, verbose=False, subset=1.0)
            
            # save sampled weight for bma
            if bma_save_path is not None:
                torch.save(sample,f'{bma_save_path}/bma_model-{i+1}.pt')
            
            # print("SWAG Sample %d/%d. EVAL" % (i + 1, bma_num_models))
            res = predict(te_loader, model, verbose=False)

            predictions = res["predictions"]
            targets = res["targets"]

            accuracy = np.mean(np.argmax(predictions, axis=1) == targets)
            nll = -np.mean(np.log(predictions[np.arange(predictions.shape[0]), targets] + eps))
            print(
                "SWAG Sample %d/%d. Accuracy: %.2f%% NLL: %.4f"
                % (i + 1, bma_num_models, accuracy * 100, nll)
            )

            swag_predictions += predictions

            ens_accuracy = np.mean(np.argmax(swag_predictions, axis=1) == targets)
            ens_nll = -np.mean(
                np.log(
                    swag_predictions[np.arange(swag_predictions.shape[0]), targets] / (i + 1)
                    + eps
                )
            )
            print(
                "Ensemble %d/%d. Accuracy: %.2f%% NLL: %.4f"
                % (i + 1, bma_num_models, ens_accuracy * 100, ens_nll)
            )

        swag_predictions /= bma_num_models

        swag_accuracy = np.mean(np.argmax(swag_predictions, axis=1) == targets)
        swag_nll = -np.mean(
            np.log(swag_predictions[np.arange(swag_predictions.shape[0]), targets] + eps)
        )

    print(f"bma Accuracy using {bma_num_models} model : {swag_accuracy * 100:.2f}% / NLL : {swag_nll:.4f}")
    return {"predictions" : swag_predictions,
            "targets" : targets,
            "bma_accuracy" : swag_accuracy,
            "nll" : swag_nll
    }



def calibration_curve(predictions, targets, num_bins):
    confidences = np.max(predictions, 1)
    step = (confidences.shape[0] + num_bins - 1) // num_bins
    bins = np.sort(confidences)[::step]
    if confidences.shape[0] % step != 1:
        bins = np.concatenate((bins, [np.max(confidences)]))
    # bins = np.linspace(0.1, 1.0, 30)
    predictions = np.argmax(predictions, 1)
    bin_lowers = bins[:-1]
    bin_uppers = bins[1:]

    accuracies = predictions == targets

    xs = []
    ys = []
    zs = []

    # ece = Variable(torch.zeros(1)).type_as(confidences)
    ece = 0.0
    for bin_lower, bin_upper in zip(bin_lowers, bin_uppers):
        # Calculated |confidence - accuracy| in each bin
        in_bin = (confidences > bin_lower) * (confidences < bin_upper)
        prop_in_bin = in_bin.mean()
        if prop_in_bin > 0:
            accuracy_in_bin = accuracies[in_bin].mean()
            avg_confidence_in_bin = confidences[in_bin].mean()
            ece += np.abs(avg_confidence_in_bin - accuracy_in_bin) * prop_in_bin
            xs.append(avg_confidence_in_bin)
            ys.append(accuracy_in_bin)
            zs.append(prop_in_bin)
    xs = np.array(xs)
    ys = np.array(ys)
    zs = np.array(zs)

    out = {"confidence": xs, "accuracy": ys, "p": zs, "ece": ece}
    return out


def save_reliability_diagram(method, optim, save_path, unc, bma=False):
    plt.clf()
    plt.plot(unc['confidence'], unc['confidence'] - unc['accuracy'], 'r', label=f'{method}-{optim}')
    plt.xlabel("confidence")
    plt.ylabel("confidence - accuracy")
    plt.axhline(y=0, color='black')
    plt.title('Reliability Diagram')
    plt.legend()
    if bma:
        plt.savefig(f'{save_path}/unc_result/{method}_{optim}_bma_reliability_diagram.png')    
        
    else:
        plt.savefig(f'{save_path}/unc_result/{method}_{optim}_reliability_diagram.png')    