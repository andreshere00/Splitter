For specific-domain adaptation, LoRA fine-tuning is commonly used in attention lay-
ers. Attention layers contain the highest number of parameters in the model since the
query, key, and value projection sets have distinct parameters. Given that these layers
store the relationships between input elements, fine-tuning only these layers is a suitable
option, being unnecessary to fine-tune the position-wised fully connected layers.

Quantization