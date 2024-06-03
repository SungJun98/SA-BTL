# ## constant
# for seed in 0 1 2
# do
# CUDA_VISIBLE_DEVICES=7 python3 hessian.py --seed=${seed} \
# --dataset=cifar10 --data_path=/data1/lsj9862/data --batch_size=1024 \
# --model=resnet18-noBN \
# --vi_load_path=/data2/lsj9862/exp_result/seed_${seed}/cifar10/scratch_resnet18-noBN/ll_vi-sgd/constant/0.01_0.001_1.0_-5.0_0.1_0.1/bma_models
# done

## cos_decay
for seed in 0 1 2
do
CUDA_VISIBLE_DEVICES=6 python3 hessian.py --seed=${seed} \
--dataset=cifar10 --data_path=/data1/lsj9862/data --batch_size=1024 \
--model=resnet18-noBN \
--vi_load_path=/data2/lsj9862/exp_result/seed_${seed}/cifar10/scratch_resnet18-noBN/ll_vi-sgd/cos_decay_1e-08/10_1e-07/0.01_0.001_1.0_-5.0_0.05_0.01/bma_models
done
