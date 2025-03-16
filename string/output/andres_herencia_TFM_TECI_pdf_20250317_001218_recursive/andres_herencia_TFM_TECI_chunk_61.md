E(w) =

1
N

N
(cid:88)

i=1

(yi − yd
i )

2

(2.4)

The minimization problem will be to find the argument which minimizes the cost

function: w∗ = arg min E(w).

This architecture is trained following an iterative scheme based on the gradient descent
[2] method, which searches in that direction where there may be a local minimum. Thus,
the weight vector is updated following the expression:

wt+1 = wt − η ·

∂E
∂w

(cid:12)
(cid:12)
(cid:12)
(cid:12)wt

(2.5)