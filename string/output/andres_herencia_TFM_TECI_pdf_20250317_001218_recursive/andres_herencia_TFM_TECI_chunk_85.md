(e) as follows:

ct =

M
(cid:88)

i=1

(e)

αtihi

The attention weight αti of the annotation hi

(e) is computed by

αti = softmax(eti) =

exp (eti)
k=1 exp (etk)

(cid:80)M

(2.12)

(2.13)

where eti is described as the alignment model, eti = a(ht−1
function. This term reflects the importance of the encoder’s annotation h(e)
decoder hidden state h(d)

(e)), being a(·) a learnable
to the next
i
[44]. It is typically param-

according to the decoder state h(d)
t−1

(d), hi

t

12