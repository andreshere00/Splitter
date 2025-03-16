This block aims to avoid gradient descent exploding and vanishing problems during each
sub-layer training phase. At the output of each sublayer, a normalization layer is applied

21

3.6. OUTPUT COMPUTATION

in addition to the input of that sublayer:

AddLayerNorm(x) = LayerNorm(x + SubLayer(x))

(3.7)

3.6 Output computation

3.6.1 Encoder and decoder output