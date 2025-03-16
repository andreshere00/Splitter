The Multi-Head Attention mechanism consists of paralleling executing the self-attention
mechanism in multiple heads, h. Each head is a subset of the embedding set which focuses
on a different input part, enhancing the model’s ability to integrate diverse information
from vector spaces of smaller dimensions [44].

MultiHead(Q, K, V ) =

where each head headT
i

is computed as:

h
(cid:13)
(cid:13)
(cid:13)
i=1

(headT

i )W O

headT

i = Attention(QW Q

i , KW K

i

, V W V
i )

(3.3)

(3.4)