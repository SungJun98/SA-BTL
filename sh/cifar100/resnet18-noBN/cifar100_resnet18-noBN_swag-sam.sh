## Constant
# for swa_start in 161
# do
#   for swa_c_epochs in 1
#   do
#     for C in 20
#     do
#       for rho in 0.05 0.1
#       do
#       CUDA_VISIBLE_DEVICES=4 python3 train.py --method=swag --optim=sam --dataset=cifar100 --data_path=/data1/lsj9862/cifar100 --batch_size=64 --model=resnet18-noBN --save_path=/data2/lsj9862/exp_result/ --lr_init=0.01 --wd=1e-3 --momentum=0.9 --epochs=300 --swa_start=${swa_start} --swa_lr=0.01 --swa_c_epochs=${swa_c_epochs} --max_num_models=${C} --use_validation --rho=${rho}
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
#       for rho in 0.05 0.1
#       do
#       CUDA_VISIBLE_DEVICES=7 python3 train.py --method=swag --optim=sam --dataset=cifar100 --data_path=/data1/lsj9862/cifar100 --batch_size=64 --model=resnet18-noBN --save_path=/data2/lsj9862/exp_result/ --lr_init=0.05 --wd=1e-3 --momentum=0.9 --epochs=300 --swa_start=${swa_start} --swa_lr=0.01 --swa_c_epochs=${swa_c_epochs} --max_num_models=${C} --scheduler=cos_anneal --t_max=300 --use_validation --rho=${rho}
#       done
#     done
#   done
# done

## SWAG lr
for swa_start in 161
do
  for swa_c_epochs in 1
  do
    for C in 20
    do
      for rho in 0.05 0.1
      do
      CUDA_VISIBLE_DEVICES=2 python3 train.py --method=swag --optim=sam --dataset=cifar100 --data_path=/data1/lsj9862/cifar100 --batch_size=64 --model=resnet18-noBN --save_path=/data2/lsj9862/exp_result/ --lr_init=0.01 --wd=1e-3 --momentum=0.9 --epochs=300 --swa_start=${swa_start} --swa_lr=??? --swa_c_epochs=${swa_c_epochs} --max_num_models=${C} --scheduler=swag_lr --use_validation --rho=${rho}
      done
    done
  done
done