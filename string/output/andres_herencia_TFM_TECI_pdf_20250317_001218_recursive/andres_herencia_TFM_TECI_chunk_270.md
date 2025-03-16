(D.1)

The update gate blends the information from the previous time step t − 1 with
the current input. This mechanism allows the model to determine the relevance of
historical information to the current context.

• Reset Gate:

rt = σ(WHR · ht−1 + WXR · xt + br)

(D.2)