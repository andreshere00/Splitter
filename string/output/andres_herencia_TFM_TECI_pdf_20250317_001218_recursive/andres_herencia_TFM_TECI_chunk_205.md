RMSnorm(x) =

√

x
σ2 + ϵ

39

5.2. TRAINING PROCESS

A very small ϵ can result in zero mappings, especially in quantized models, while
higher values can introduce bias.

• optim: