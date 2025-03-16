Quantization

Even with these modifications, fine-tuning may still be time-consuming due to weight
computations. Subsequently, the LoRA approach can be combined with quantization.
Quantization reduces the precision of the model’s weights, decreasing model size and
computational requirements without significantly impacting performance. For instance,
converting a 32-bit floating point to a lower-precision representation, such as a 16-bit or
8-bit floating point.