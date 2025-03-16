(C.5)

(C.6)

This gate decides which part of the cell state will be passed to the output. The
sigmoid function σ(·) determines which parts of the cell state will be used mean-
while the tanh(·) function provides a normalized version of the cell state, which is
multiplied by the value processed by the sigmoid to return the final output ht of
the LSTM block for that time step t.