After some experiments, the candidate model with the best performance has been selected.
In all experiments, the number of layers and their dimensions are consistent with the base
model. The selected model has the following training parameters and values:

Parameter
target_modules
lora_r
lora_alpha
lora_dropout
rms_norm_eps
optim
weight_decay
max_grad_norm
warmup_ratio
lr_scheduler_type "cosine"1
num_train_epochs

Value
{"q_proj", "v_proj"}1
641
161
0.11
1e-52
"adamw_32bits"1
0.0012
0.31
0.032