Loading an LLM model based on LLaMA requires significant memory:

Memory usage (GB) = Number of parameters (billions) × Parameters (bytes)

(4.7)

For instance, a model with 7 billion parameters requires 28 GB of memory at maximum
precision. So, if 4-bit quantization is used, reduces memory usage to 3.5 GB, significantly

33

4.2. LLM CUSTOMIZATION TECHNIQUES

lowering computational costs. This is critical for GPU computations, which are expensive.