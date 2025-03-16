by the expression:

t = RNN(e)(xt, h(e)
h(e)

t−1)

(2.8)

Note that h(e)

0 = 0. In MT context, xN is always a <eos> (end of string) indicator.
• Decoder output: corresponds to the last hidden state of the decoder, computed

by the expression:

yt = softmax(WHOht

(d) + bO).

ht

(d) = RNN(d)(yt−1, h(e)

t−1)

(2.9)

(2.10)

In MT context, y0 is always a <bos> (beginning of string) indicator.
Since (WHOht
(f : RM → R) must be applied.