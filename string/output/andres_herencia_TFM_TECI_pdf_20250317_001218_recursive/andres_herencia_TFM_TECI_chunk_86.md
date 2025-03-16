(d), hi

t

12

2.4. ARCHITECTURES WITH ATTENTION MECHANISMS

eterized by a small neural network (often a FNN). The alignment model scores the match
between an input position i and the current time step t, guiding the decoder’s attention
to the most relevant parts of the input sequence when generating each word in the output
sequence.

After that, the RNN outputs the most probable symbol yt at time step t as:

p(yt|y1, . . . , yM; xt) = RNN(d)(ct)

(2.14)