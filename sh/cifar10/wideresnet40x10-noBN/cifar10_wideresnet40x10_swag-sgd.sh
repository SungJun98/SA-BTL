## Constant
# for swa_start in 101 161 201
# do
# for swa_c_epochs in 1 3 5
# do
# for C in 10 20 30
# do
# CUDA_VISIBLE_DEVICES=1 python3 train.py --method=swag --optim=sgd --dataset=cifar10 --data_path=/data1/lsj9862/cifar10 --batch_size=256 --model=wideresnet40x10-noBN --save_path=/mlainas/lsj9862/exp_result/ --lr_init=0.05 --wd=5e-4 --momentum=0.9 --epochs=300 --swa_start=${swa_start} --swa_lr=0.01 --swa_c_epochs=${swa_c_epochs} --max_num_models=${C} --use_validation --metrics_step
# done
# done
# done



## Cos Anneal
# for swa_start in 101 161 201
# do
# for swa_c_epochs in 1 3 5
# do
# for C in 10 20 30
# do
# CUDA_VISIBLE_DEVICES=6 python3 train.py --method=swag --optim=sgd --dataset=cifar10 --data_path=/data1/lsj9862/cifar10 --batch_size=256 --model=wideresnet40x10-noBN --save_path=/data1/lsj9862/exp_result/ --lr_init=0.1 --wd=5e-4 --momentum=0.9 --epochs=300 --swa_start=${swa_start} --swa_lr=0.01 --swa_c_epochs=${swa_c_epochs} --max_num_models=${C} --scheduler=cos_anneal --t_max=300 --use_validation --metrics_step
# done
# done
# done



## SWAG lr
for swa_start in 101 161 201
do
for swa_c_epochs in 1 # 1 3 5
do
for C in 30 # 10 20 30
do
CUDA_VISIBLE_DEVICES=1 python3 train.py --method=swag --optim=sgd --dataset=cifar10 --data_path=/data1/lsj9862/cifar10 --batch_size=256 --model=wideresnet40x10-noBN --save_path=/data1/lsj9862/exp_result/ --lr_init=0.05 --wd=5e-4 --momentum=0.9 --epochs=300 --swa_start=${swa_start} --swa_lr=0.01 --swa_c_epochs=${swa_c_epochs} --max_num_models=${C} --scheduler=swag_lr --use_validation --metrics_step
done
done
done