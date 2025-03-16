4. lora_dropout : controls the fraction of LoRA layer outputs set to zero dur-
ing training, i.e., the proportion of the original parameters that will not be re-
parametrized. It acts as a LoRA regularization term.

Trainer arguments

LLaMA architectures (as all the previous architectures) are trained using gradient-descent-
based methods. The main trainer parameters are:

• rms_norm_eps: a regularization term for the RMS Normalization Layers which

avoid divisions by zero:

RMSnorm(x) =

√