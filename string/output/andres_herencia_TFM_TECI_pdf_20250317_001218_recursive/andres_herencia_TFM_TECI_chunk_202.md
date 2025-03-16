The virtual machines used for the training process had between 16 GB vRAM and 24 GB
RAM. The complete model requires 28 GB of RAM for deployment and over 7 GB of ad-
ditional vRAM for training (depending on the batch size and other trainer’s parameters).
Hence, a 4-bit quantization method is employed, reducing the needed vRAM requirement
from 28 GB to 3.5 GB.

LoRA parameters

1. target_modules: specifies in which elements or layers LoRA is applied.