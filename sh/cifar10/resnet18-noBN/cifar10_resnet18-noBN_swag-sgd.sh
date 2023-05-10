## Constant
# for swa_start in 161
# do
#   for swa_c_epochs in 1
#   do
#     for C in 20
#     do
#       for swa_lr in 0.005 0.001
#       do
#       CUDA_VISIBLE_DEVICES=4 python3 train.py --method=swag --optim=sgd --dataset=cifar10 --data_path=/data1/lsj9862/cifar10 --batch_size=64 --model=resnet18-noBN --save_path=/data2/lsj9862/exp_result --lr_init=0.01 --wd=5e-4 --momentum=0.9 --epochs=300 --swa_start=${swa_start} --swa_lr=${swa_lr} --swa_c_epochs=${swa_c_epochs} --max_num_models=${C} --use_validation
#       done
#     done
#   done
# done



## Cosine Annealing
# for swa_start in 161
# do
#   for swa_c_epochs in 1
#   do
#     for C in 20
#     do
#       for swa_lr in 0.005 0.001
#       do
#       CUDA_VISIBLE_DEVICES=3 python3 train.py --method=swag --optim=sgd --dataset=cifar10 --data_path=/data1/lsj9862/cifar10 --batch_size=64 --model=resnet18-noBN --save_path=/data2/lsj9862/exp_result --lr_init=0.01 --wd=1e-3 --momentum=0.9 --epochs=300 --swa_start=${swa_start} --swa_lr=${swa_lr} --swa_c_epochs=${swa_c_epochs} --max_num_models=${C} --scheduler=cos_anneal --use_validation --t_max=300
#       done
#     done
#   done
# done




## SWAG LR
# for swa_start in 161
# do
#   for swa_c_epochs in 1
#   do
#     for C in 20
#     do
#       for swa_lr in 0.005 0.001
#       do
#       CUDA_VISIBLE_DEVICES=2 python3 train.py --method=swag --optim=sgd --dataset=cifar10 --data_path=/data1/lsj9862/cifar10 --batch_size=64 --model=resnet18-noBN --save_path=/data2/lsj9862/exp_result --lr_init=0.01 --wd=5e-4 --momentum=0.9 --epochs=300 --swa_start=${swa_start} --swa_lr=${swa_lr} --swa_c_epochs=${swa_c_epochs} --max_num_models=${C} --scheduler=swag_lr --use_validation
#       done
#     done
#   done
# done