# for seed in 0 1 2
# do
# CUDA_VISIBLE_DEVICES=7 python3 hessian.py --dataset=cifar10 --data_path=/data1/lsj9862/data/cifar10/ --use_validation --seed=${seed} \
# --model=resnet18 --pre_trained  --swag_load_path="/data2/lsj9862/exp_result/seed_${seed}/cifar10/pretrained_resnet18/swag-sgd/constant/0.01_0.0005_3_76_1/bma_models/"
# done

# for seed in 0 1 2
# do
# CUDA_VISIBLE_DEVICES=6 python3 hessian.py --dataset=cifar10 --data_path=/data1/lsj9862/data/cifar10/ --use_validation --seed=${seed} \
# --model=resnet18 --pre_trained  --swag_load_path="/data2/lsj9862/exp_result/seed_${seed}/cifar10/pretrained_resnet18/swag-sgd/cos_decay_1e-08/10_1e-07/0.01_0.001_3_101_1/bma_models/"
# done

for seed in 0 1 2
do
CUDA_VISIBLE_DEVICES=5 python3 hessian.py --dataset=cifar10 --data_path=/data1/lsj9862/data/cifar10/ --use_validation --seed=${seed} \
--model=resnet18 --pre_trained  --swag_load_path="/data2/lsj9862/exp_result/seed_${seed}/cifar10/pretrained_resnet18/swag-sgd/swag_lr_0.001/0.005_0.005_3_101_1/bma_models/"
done