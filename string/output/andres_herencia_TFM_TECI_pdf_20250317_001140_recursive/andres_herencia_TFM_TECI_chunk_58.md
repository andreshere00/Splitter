Output computation

Assume a MLP of L layers. a(l) is defined as the activation term of layer l, a(l) =
f (l)(w(l)a(l−1) + b(l)) where the first term is a(1) = f (1)(w(1)x + b(1)). Note that it is the
expression obtained in the equation 2.1 but generalized for all the neurons in the first
layer.

The expression in the output layer can be obtained by:

y = f (L)(w(L)a(L) + b(L))

(2.3)

Equivalently:

y = f (L)(w(L) · f (L−1)(w(L−1) . . . (w(1) · x + b(1)) + b(2)) + · · · + b(L−1)) + b(L))