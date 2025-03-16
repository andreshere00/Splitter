3.1.1 Encoder

The encoder is composed of a stack of N = 6 identical layers. Each layer has two sub-
layers: the first has a Multi-Head Attention layer, and the second has a position-wise
fully connected neural network. Add and normalization mechanisms are provided at the
output of both sub-layers (avoiding gradient descent problems). In the next subsections
will be explained these mechanisms. All the sub-layers in the model produce outputs of
dimension d = 512.