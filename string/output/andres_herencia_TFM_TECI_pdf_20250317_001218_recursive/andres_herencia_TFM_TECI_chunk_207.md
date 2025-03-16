• weight_decay: states for the L2 regularization term λ over the loss function:

Lnew (W ) = Loriginal (W ) + λW T W

A relatively low value prevents the model from over-fitting. A high value of this
parameter may cause under-fitting. This term is uniquely presented in AdamW and
AdamWeightDecay methods. [21]