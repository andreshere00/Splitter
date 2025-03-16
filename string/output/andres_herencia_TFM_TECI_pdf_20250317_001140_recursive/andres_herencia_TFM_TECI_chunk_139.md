Using a linear argument of the sinusoidal function preserves relative positions because
the angle separating each pair of tokens remains constant regardless of their sequence
position. This method also provides stability to the vectors, as appending elements to
the end of the input sequence does not affect the existing embeddings, thereby enabling
an effective query-key caching technique.

3.7.2 SwiGLU activation function in feedforward layers