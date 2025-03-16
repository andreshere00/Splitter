←−
h2
(e),

(e),
−→
h1

When all the hidden states are computed in each direction, an annotation for each xi is
(e).
obtained concatenating both priorly computed hidden states: hi
The annotations are, in fact, the codification of the inputs and at the same time, the

(e)]T = hi

←−
hi

−→
hi

= [

(e);

(e)

11

2.4. ARCHITECTURES WITH ATTENTION MECHANISMS

Figure 2.7: RNNsearch architecture. Decoder is shown only for time step t.

hidden states of the bidirectional RNN [4]:

(h1