5.3.1 BERT Score

Given a reference sequence x = ⟨x1, x2, . . . , xN ⟩ and a target sequence ˆx = ⟨ˆx1, ˆx2, . . . ,
ˆxM ⟩, where each element is a token, BERT models are used to obtain their contextual
embeddings. The similarity between the two sequences is computed using a pairwise cosine
similarity metric [41]. For every token pair (xi, ˆxj), the cosine similarity is calculated as
follows:

Cosine similarity =

∈ [0, 1]

(5.1)

xT
i · ˆxj
||xi|| · ||ˆxj||