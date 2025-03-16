• optim:

the argument that defines the optimization method used to minimize
the loss function.
It can be three different methods: AdamW, AdaFactor, and
AdamWeightDecay. All of them are based on the Adam optimization method,
[29] a Stochastic Gradient Descent technique with variable learning rate η (see sec-
tion 2.1.1). While Adafactor is more computationally efficient, it does not present
regularization terms as the AdamW and AdaFactor optimizer methods.