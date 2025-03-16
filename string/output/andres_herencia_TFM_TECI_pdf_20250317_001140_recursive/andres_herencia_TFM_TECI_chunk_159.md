To ensure that only the most relevant documents are selected in response to the query,
an attention mechanism is employed. In the original paper [34], dot-product is used, but it
could be any attention function. This function produces a probability distribution pη(z|x)
which explains the relationship between the query and the document. Analytically:

d(z) = BERT(d(z))
q(x) = BERT(q(x))

pη(z|x) ∝ exp

(cid:16)

(cid:17)
d(z)⊤q(x)

(4.1)

(4.2)

(4.3)