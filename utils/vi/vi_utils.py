import numpy as np
import torch
from ..swag.swag_utils import predict, flatten
import utils.utils as utils
from bayesian_torch.models.dnn_to_bnn import get_kl_loss
    
def get_vi_mean_vector(model):
    """
    Get Mean parameters in Variational Inference model
    """
    mean_list = []
    for name, param in model.named_parameters():
        if "rho" not in name:
            mean_list.append(param)
    return flatten(mean_list)
            
            
def get_vi_variance_vector(model, delta=0.2):
    """
    Get (Diagonal) Variance Parameters in Variatioanl Inference model
    """
    var_list = []
    for name, param in model.named_parameters():
        if "rho" in name:            
            var_list.append(torch.log(1+torch.exp(param)))  # rho to variance
        elif ("mu" not in name) and ("rho" not in name):
            var_list.append(torch.zeros_like(param))
    return flatten(var_list)


# train variational inference
def train_vi(dataloader, model, criterion, optimizer, device, scaler, batch_size):
    loss_sum = 0.0
    correct = 0.0

    num_objects_current = 0
    num_batches = len(dataloader)

    model.train()
    for batch, (X, y) in enumerate(dataloader):
        X, y = X.to(device), y.to(device)

        if scaler is not None:
            with torch.cuda.amp.autocast():
                pred = model(X)
                kl = get_kl_loss(model)
                loss = criterion(pred, y)
                loss += kl / batch_size
                
                scaler.scale(loss).backward()
                scaler.step(optimizer)  # optimizer.step()
                scaler.update()
                optimizer.zero_grad()
        else:
            pred = model(X)
            kl = get_kl_loss(model)
            loss = criterion(pred, y)
            loss += kl/batch_size
            
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()
        
        correct += (pred.argmax(1) == y).type(torch.float).sum().item()
        loss_sum += loss.data.item() * X.size(0)
        num_objects_current += X.size(0)
    return {
        "loss": loss_sum / num_objects_current,
        "accuracy": correct / num_objects_current * 100.0,
    }




def eval_vi(val_loader, model, num_classes, criterion, val_mc_num, num_bins=50, eps=1e-8):
    mc_predictions = np.zeros((len(val_loader.dataset), num_classes))
    model.eval()
    with torch.no_grad():
        if val_mc_num == 1:
            res = predict(val_loader, model, verbose=False)
            predictions = res["predictions"]; targets = res["targets"]
            loss = criterion(torch.tensor(predictions), torch.tensor(targets)).item()
            accuracy = np.mean(np.argmax(predictions, axis=1) == targets)
            nll = -np.mean(np.log(predictions[np.arange(predictions.shape[0]), targets] + eps))
            ece = utils.calibration_curve(predictions, targets, num_bins)['ece']
            
        else:
            for i in range(val_mc_num):
                res = predict(val_loader, model, verbose=False)
                mc_predictions += res["predictions"]
            mc_predictions /= val_mc_num

            loss = criterion(torch.tensor(mc_predictions), torch.tensor(res['targets'])).item()
            accuracy = np.mean(np.argmax(mc_predictions, axis=1) == res["targets"])
            nll = -np.mean(np.log(mc_predictions[np.arange(mc_predictions.shape[0]), res["targets"]] + eps))
            ece = utils.calibration_curve(mc_predictions, res["targets"], num_bins)['ece']
            
            predictions = mc_predictions
            targets = res["targets"]
            
    return {
        "predictions" : predictions,
        "targets" : targets,
        "loss" : loss, # loss_sum / num_objects_total,
        "accuracy" : accuracy * 100.0,
        "nll" : nll,
        "ece" : ece,
    }
    
    
    
def bma_vi(te_loader, mean, variance, model, method, bma_num_models, num_classes, bma_save_path=None, eps=1e-8):
    '''
    run bayesian model averaging in test step
    '''
    ## Check whether it's last layer or not
    model_shape = list()
    for p in model.parameters():
        model_shape.append(p.shape)
    
    if "last" in method:
        last = True
        model_shape = model_shape[-2:]
        for name, _ in model.named_modules():
            last_layer_name = name
    else:
        last = False
    
    bma_predictions = np.zeros((len(te_loader.dataset), num_classes))
    with torch.no_grad():
        for i in range(bma_num_models):
            if i == 0:
               sample = mean
            else:
                # sampling z 
                sample = mean + variance * torch.randn_like(variance, requires_grad=False)

            sample = utils.unflatten_like_size(sample, model_shape)
            sample = utils.list_to_state_dict(model, sample, last, last_layer_name)
            model.load_state_dict(sample, strict=False)
            
            # save sampled weight for bma
            if bma_save_path is not None:
                torch.save(sample, f'{bma_save_path}/bma_model-{i}.pt')
 
            res = predict(te_loader, model, verbose=False)
            predictions = res["predictions"];targets = res["targets"]

            accuracy = np.mean(np.argmax(predictions, axis=1) == targets)
            nll = -np.mean(np.log(predictions[np.arange(predictions.shape[0]), targets] + eps))
            print(
                "Sample %d/%d. Accuracy: %.2f%% NLL: %.4f"
                % (i + 1, bma_num_models, accuracy * 100, nll)
            )

            bma_predictions += predictions

            ens_accuracy = np.mean(np.argmax(bma_predictions, axis=1) == targets)
            ens_nll = -np.mean(
                np.log(
                    bma_predictions[np.arange(bma_predictions.shape[0]), targets] / (i + 1)
                    + eps
                )
            )
            print(
                "Ensemble %d/%d. Accuracy: %.2f%% NLL: %.4f"
                % (i + 1, bma_num_models, ens_accuracy * 100, ens_nll)
            )

        bma_predictions /= bma_num_models

        bma_accuracy = np.mean(np.argmax(bma_predictions, axis=1) == targets)
        bma_nll = -np.mean(
            np.log(bma_predictions[np.arange(bma_predictions.shape[0]), targets] + eps)
        )
    
    print(f"bma Accuracy using {bma_num_models} model : {bma_accuracy * 100:.2f}% / NLL : {bma_nll:.4f}")
    return {"predictions" : bma_predictions,
            "targets" : targets,
            "bma_accuracy" : bma_accuracy,
            "nll" : bma_nll
    }