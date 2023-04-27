## Cos Annealing
for rho in 0.05 0.1
do
CUDA_VISIBLE_DEVICES=7 python3 train.py --method=dnn --optim=sam --dataset=cifar100 --data_path=/data1/lsj9862/data/cifar100 --batch_size=64 --model=resnet18 --save_path=/data2/lsj9862/exp_result/ --lr_init=0.1 --momentum=0.9 --wd=5e-4 --epochs=300 --use_validation --scheduler=cos_anneal --t_max=300 --rho=${rho}
done

## SWAG lr
for rho in 0.05 0.1
do
CUDA_VISIBLE_DEVICES=4 python3 train.py --method=dnn --optim=sam --dataset=cifar100 --data_path=/data1/lsj9862/data/cifar100 --batch_size=64 --model=resnet18 --save_path=/data2/lsj9862/exp_result/ --lr_init=0.05 --wd=1e-3 --momentum=0.9 --epochs=300 --use_validation --scheduler=swag_lr --rho=${rho}
done