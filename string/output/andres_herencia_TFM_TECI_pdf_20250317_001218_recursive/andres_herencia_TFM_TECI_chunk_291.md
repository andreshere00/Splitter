NOTE: stemming can be used alternatively to lemmatization, but it has less accuracy

since it can invent words during the tokenization process.

XII

Appendix F

Transformer position encoding

Let t the desired position, in an input sentence, ⃗pt ∈ Rd its corresponding encoding and
d = dmodel the dimension of the embedding vector space. Then, for each embedding
position, the position encoding g : N → Rd is given by the expression:

⃗p(i)
t = g(t)(i) =




sin (ωk · t) ,

if i = 2k

