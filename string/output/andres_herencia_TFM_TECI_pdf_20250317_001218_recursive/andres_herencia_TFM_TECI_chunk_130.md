The encoder’s final output is a vector sequence, where each vector corresponds to an input
token enriched with contextual information given by the attention mechanism.

t = LayerNorm(s(e)
z(e)

t + F N N (s(e)

t ))

(3.8)

t

where s(e)
LayerNorm function. F N N (s(e)
layers.

is the output of the last sub-layer at the time step t, normalized via the
t ) corresponds to the output of the encoder’s feed-forward

The decoder’s output is given by the vector sequence processed by the MHA mecha-