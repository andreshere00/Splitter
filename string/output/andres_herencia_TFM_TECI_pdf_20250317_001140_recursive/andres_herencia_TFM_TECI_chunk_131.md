nism with the context provided by the masked Multi-Head Attention layer.

t = LayerNorm(s(d)
z(d)

t + F N N (s(d)

t ))

(3.9)

where s(d)

t

is the output of the last sub-layer.

3.6.2 Transformer output

Finally, the transformer returns a sequence vector. This vector represents the probability
distribution over the vocabulary used in the dictionary (embeddings) model, indicating
the next word to produce in the output sequence (i.e., a a posteriori Bayesian distribution,
see Appendix B).