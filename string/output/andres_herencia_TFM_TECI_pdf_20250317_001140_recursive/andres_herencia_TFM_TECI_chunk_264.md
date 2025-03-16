(C.2)

(C.3)

This gate determines what new information will be stored in the cell state. The σ

V

function, which decides which values to update, and tanh, which creates a vector of
new candidate values ˜Ct that could be added to the state.

• Control Gate:

Ct = ft ∗ Ct−1 + it ∗ ˜Ct

(C.4)