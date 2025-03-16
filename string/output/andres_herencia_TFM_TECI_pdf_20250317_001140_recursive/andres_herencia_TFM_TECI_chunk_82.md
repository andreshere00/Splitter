Encoder

The BiRNN for a time step t does not exclusively take the previous and current inputs
It
but, computes the hidden states by taking all the future and previous input data.
is trained in two directions: backward, from xN to x1, denoting the hidden states as
←−
(e)}; and forward, from x1 to xN denoting the hidden states
(e), . . . ,
ht
−→
−→
as
(e)}. This process is known as a Bidirectional Backward
hN
h2
Propagation (B-BP).

←−
h1
(e) = {

←−
hN
(e), . . . ,

(e) = {
−→
ht

←−
h2
(e),