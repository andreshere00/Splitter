Additionally, LLaMA has some changes in comparison with the architecture model: (i)
pre-normalization, the normalization block uses RMS normalization and it is positioned at
the input of each block; (ii) the use of another activation function in the feed-forward lay-
ers, Swish-Gated Linear Unit (SwiGLU); and (iii), a new attention mechanism, Grouped
Query Attention (GQA), but it is solely presented in the 70 billion parameter version.