Input data is summed and weighted via the ADAptative LINear Element (ADALINE).
This component adds a bias term, denoted by b. Then, this data is processed by an acti-
vation function, a generally monotonous, continuous, bounded, and non-linear application
used to model complex relationships between input and output data.

In the specific case of simple perception (which acts as a linear binary classification

machine), the sign function is used,

sgn(x) =




1,



−1,

if x ≥ 0

if x < 0