In section 2.4, the most basic version of the attention mechanism has been reviewed. The
Transformer introduces two new mechanisms: self-attention and Multi-Head Attention
(MHA), which are explained below.

3.3.1 Self-attention

In this mechanism, the embeddings set E is divided into three different sets of same
dimension k × d: the query Q = {q1, q2, . . . , qk}, the key K = {k1, k2, . . . , kk}, and the
value V = {v1, v2, . . . , vk}.