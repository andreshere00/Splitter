(3.3)

(3.4)

W Q
i

, W K
i

, and W V
i

are the projection matrices for queries, keys, and values, respec-
tively, for the i-th head. W O is the output projection matrix that combines the outputs
of all heads. (cid:13)
h
i=1 xi is the concatenation operator for xi from index i = 1 to i = h.
(cid:13)

In the Google’s paper [61], each embedding is divided into h = 8 attention heads,
8 = 64.

so the dimension of each query, key, and value set is p × d, where p = k

h = 512

19