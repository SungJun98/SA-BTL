for seed in 0 # 1 2
do
CUDA_VISIBLE_DEVICES=2 python3 run_baseline.py --method=dnn --optim=bsam --dataset=cifar100 --use_validation --dat_per_cls=10 \
--model=resnet18 --pre_trained --lr_init=5e-1 --wd=1e-4 --epochs=100 --seed=${seed} --ignore_wandb --rho=0.001 \
--scheduler=cos_decay --lr_min=1e-8 --warmup_t=20 --warmup_lr_init=1e-7 --no_amp --noise_scale=1e-5
done

# ------------------------------
# Set sgd optimizer with lr_init 0.005 / wd 0.0001 / momentum 0.9 / rho 0.05 / noise_scale 0.0001
# ------------------------------
# Set constant lr scheduler
# ------------------------------
# Set AMP Scaler for sgd
# ------------------------------
# Start training dnn with sgd optimizer from 1 epoch!
# -------  --------  --------  ---------  --------  ----------  ---------  ---------  ---------  --------
#   epoch  method          lr    tr_loss    tr_acc    val_loss    val_acc    val_nll    val_ece      time
# -------  --------  --------  ---------  --------  ----------  ---------  ---------  ---------  --------
#       1  dnn-sgd     0.0050     4.8229    0.6000      4.7097     0.9000     4.7097     0.0202    6.9864
#       2  dnn-sgd     0.0050     4.7064    1.3000      4.6582     1.2200     4.6582     0.0147    5.0567
#       3  dnn-sgd     0.0050     4.6195    1.3000      4.5981     1.6400     4.5981     0.0097    4.8238
#       4  dnn-sgd     0.0050     4.5229    3.1000      4.5491     2.0800     4.5491     0.0083    5.0628
#       5  dnn-sgd     0.0050     4.4262    4.5000      4.4957     2.9200     4.4957     0.0046    5.3109
#       6  dnn-sgd     0.0050     4.3450    6.3000      4.4357     4.6000     4.4357     0.0180    5.1926
#       7  dnn-sgd     0.0050     4.2719    7.9000      4.3572     5.8200     4.3572     0.0278    4.8881
#       8  dnn-sgd     0.0050     4.1727    9.9000      4.2842     7.1600     4.2842     0.0372    5.1083
#       9  dnn-sgd     0.0050     4.0580   13.4000      4.2210     8.0800     4.2210     0.0405    4.9151
#      10  dnn-sgd     0.0050     3.9460   16.3000      4.1424    10.0200     4.1424     0.0548    4.9248
# -------  --------  --------  ---------  --------  ----------  ---------  ---------  ---------  --------
#   epoch  method          lr    tr_loss    tr_acc    val_loss    val_acc    val_nll    val_ece      time
# -------  --------  --------  ---------  --------  ----------  ---------  ---------  ---------  --------
#      11  dnn-sgd     0.0050     3.8643   18.7000      4.0605    11.2800     4.0605     0.0617    4.9410
#      12  dnn-sgd     0.0050     3.7170   22.8000      3.9952    11.6800     3.9952     0.0584    4.8910
#      13  dnn-sgd     0.0050     3.6138   24.0000      3.9248    13.4200     3.9248     0.0679    5.2775
#      14  dnn-sgd     0.0050     3.5172   26.5000      3.8558    14.2600     3.8558     0.0689    4.8985
#      15  dnn-sgd     0.0050     3.4004   30.8000      3.7931    15.3400     3.7931     0.0745    4.9959
#      16  dnn-sgd     0.0050     3.3019   33.4000      3.7308    16.5200     3.7308     0.0795    4.8706
#      17  dnn-sgd     0.0050     3.1883   34.2000      3.6690    17.2200     3.6690     0.0792    4.8787
#      18  dnn-sgd     0.0050     3.1520   36.1000      3.5886    18.1400     3.5886     0.0816    4.9431
#      19  dnn-sgd     0.0050     3.0115   39.1000      3.5246    19.5200     3.5246     0.0847    4.7556
#      20  dnn-sgd     0.0050     2.9487   38.5000      3.4660    20.2800     3.4660     0.0828    4.8024