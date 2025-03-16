These functions compute the attention scores (usually by a FNN using the back-
propagation method). When weighted by the values, marks the importance of each em-
bedding concerning the others:

S = f (Q, K, V ) = f (Q, K)V

(3.2)