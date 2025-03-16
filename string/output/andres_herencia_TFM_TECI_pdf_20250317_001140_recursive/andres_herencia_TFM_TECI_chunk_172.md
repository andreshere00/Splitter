Low Rank Adapters (LoRA) and Quantized PEFT Methods

An adapter adds extra layers positioned after the original layers. During training,
the pre-trained model weights remain frozen, and only the adapter weights are updated
(Figure 4.4a). Although this method is effective for training, it increases latency during
inference or text generation tasks due to using additional layers (W ′ = W + ∆W ).