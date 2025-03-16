Masking is implemented by modifying the attention scores before they are processed
through the softmax function. The scores corresponding to future positions are set to −∞
(or a high negative number) and 0 otherwise. Remembering the softmax function shape,
a sufficiently negative argument returns a null value, so in practical terms, no attention

20

3.4. POSITION-WISED FEED-FORWARD LAYERS

is paid to that position. [61] Analytically:

Attention(Q, K, V ) = softmax

(cid:18) QK T
√
dk