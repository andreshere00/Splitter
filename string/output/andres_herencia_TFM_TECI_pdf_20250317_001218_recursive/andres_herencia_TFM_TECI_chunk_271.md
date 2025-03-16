(D.2)

The reset gate acts as a forgetting or memory mechanism. This gate allows the ANN
to drop information no longer relevant to the current problem, enhancing the time
relationships between input elements and better handling varying sequence lengths.

VII

• Candidate Activation:

˜ht = tanh(WHH · (rt ∗ ht−1) + WHX · xt + bc)

(D.3)