1 , z(e)

3.1.2 Decoder

Analogously, the decoder is composed of a stack of N = 6 layers. It is built with the same
sub-layers as the encoder but priory introduces another sub-layer which defines a masked
MHA mechanism. Combined with offsetting the output embeddings by one position, this
masking ensures that the actual predictions at position t can depend only on the outputs
at previous positions (see section 3.3.3).

The input of this block is represented with a vector z(d)