For example, consider the reference sentence “The weather is cold today” and the target
sequence “It is freezing today”. Despite only two words being identical, their contextual
information is similar, resulting in a high similarity score of 0.8663093.

By relating each token from both sentences, a similarity matrix is built. From this

matrix, precision (PBERT), recall (RBERT), and F1 (FBERT) scores are computed:

PBERT =

RBERT =

1
|ˆx|

1
|x|

(cid:88)

ˆxj ∈ˆx
(cid:88)

xi∈x

max
xi∈x