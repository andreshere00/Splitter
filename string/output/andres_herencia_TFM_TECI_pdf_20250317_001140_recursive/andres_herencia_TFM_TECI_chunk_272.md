(D.3)

The candidate activation represents a proposed update to the GRU unit’s activation
term, combining new input information with selectively retained previous informa-
tion. This update is moderated by the reset gate, determining the extension to
which previous activations are incorporated into the candidate.

• Final Activation:

ht = (1 − zt) ∗ ht−1 + zt ∗ ˜ht

(D.4)