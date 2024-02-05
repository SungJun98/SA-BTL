## DNN SGD
for seed in 0 1 2
do
CUDA_VISIBLE_DEVICES=0 python3 run_baseline.py --method=dnn --optim=sgd --dataset=cifar10 --data_path=/data2/lsj9862/data/ --use_validation --dat_per_cls=10 \
--model=resnet18 --pre_trained --lr_init=5e-3 --epochs=100 --wd=1e-3 \
--scheduler=cos_decay --lr_min=1e-8 --warmup_t=10 --warmup_lr_init=1e-7  --seed=${seed} \
--save_path=/data2/lsj9862/best_result
done

## DNN SAM
for seed in 0 1 2
do
CUDA_VISIBLE_DEVICES=0 python3 run_baseline.py --method=dnn --optim=sam --rho=0.1 --dataset=cifar10 --data_path=/data1/lsj9862/data/ --use_validation --dat_per_cls=10 \
--model=resnet18 --pre_trained --lr_init=1e-2 --epochs=100 --wd=1e-4 \
--scheduler=cos_decay --lr_min=1e-8 --warmup_t=10 --warmup_lr_init=1e-7  --seed=${seed} \
--save_path=/data2/lsj9862/best_result
done

## SWAG SGD
for seed in 0 1 2
do
CUDA_VISIBLE_DEVICES=0 python3 run_baseline.py --method=swag --dataset=cifar10 --data_path=/data1/lsj9862/data/ --use_validation --dat_per_cls=10 \
--model=resnet18 --pre_trained --optim=sgd --epochs=150 --lr_init=5e-3 --wd=1e-5 \
--scheduler=cos_decay --swa_start=76 --swa_c_epochs=2 --seed=${seed} \
--save_path=/data2/lsj9862/best_result

done

## VI SGD
for seed in 0 1 2
do
CUDA_VISIBLE_DEVICES=0 python3 run_baseline.py --dataset=cifar10 --data_path=/data1/lsj9862/data --use_validation --dat_per_cls=10 \
--method=vi --model=resnet18 --pre_trained --optim=sgd --lr_init=1e-2 --wd=1e-4 --epoch=100 --scheduler=cos_decay  \
--vi_moped_delta=0.1 --kl_beta=0.1 \
--seed=${seed} \
--save_path=/data2/lsj9862/best_result
done

## SWAG SAM
for seed in 0 1 2
do
CUDA_VISIBLE_DEVICES=0 python3 run_baseline.py --method=swag --dataset=cifar10 --data_path=/data1/lsj9862/data --use_validation --dat_per_cls=10 \
--model=resnet18 --pre_trained --optim=sam --rho=0.05 --epochs=150 --lr_init=5e-3 --wd=5e-4 \
--scheduler=cos_decay --swa_start=76 --swa_c_epochs=3 --seed=${seed} \
--save_path=/data2/lsj9862/best_result
done