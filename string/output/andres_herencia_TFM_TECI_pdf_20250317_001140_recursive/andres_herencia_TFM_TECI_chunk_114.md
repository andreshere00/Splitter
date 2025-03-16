√

)

• Similarity (normalized cosine similarity ): f (Q, K) = softmax

(cid:16) Q·KT
∥Q∥∥K∥

(cid:17)

• Location-based: f (Q, K) = f (Q)

Note that WQ, WK, and WV are learnable parameters, corresponding to the matrix
weights of K, Q, and V , respectively, b is a bias term and dk is the dimension of the key
vector k ∈ K.