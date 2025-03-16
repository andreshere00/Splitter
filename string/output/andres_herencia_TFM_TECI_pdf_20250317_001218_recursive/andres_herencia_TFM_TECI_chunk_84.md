(h1

(e), . . . , hN

(e)) = BiRNN(e)(x1, . . . , xN)

(2.11)

When hidden states are computed, this information is sent to the decoder.

Decoder

The decoder is built with an attention block and a unidirectional RNN. In SMT problems,
the attention block captures the text context in a vector, representing the relationship
between the current output vector and each input term. So, at a time step t, the context
vector ct is computed as a weighted sum of the weighted annotations hi