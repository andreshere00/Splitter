(C.4)

This gate updates the cell state Ct by merging past and new information. It multi-
plies the previous state Ct−1 by the result of the forget gate (deciding what to forget)
and adds the product of the input gate and the update candidates ˜Ct (deciding what
new information to add).

• Output Gate:

yt = ot = σ(WHO · ht−1 + WHX · xt + bo),

ht = ot · tanh(Ct)

(C.5)

(C.6)