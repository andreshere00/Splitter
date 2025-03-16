Based on the diagram in Figure C.1, each of the gates can be explained as follows:

• Forget Gate:

ft = σ(WHF · ht−1 + WXF · xt + bF )

(C.1)

This gate decides which information from the previous cell state Ct−1 should be
discarded or retained. If the output of the forget gate is close to 1, the information
is retained; if it is close to 0, it is forgotten.

• Input Gate:

it = σ(WHI · ht−1 + WHX · xt + bI),
˜Ct = tanh(WHC · ht−1 + WXC · xt + bC)

(C.2)

(C.3)