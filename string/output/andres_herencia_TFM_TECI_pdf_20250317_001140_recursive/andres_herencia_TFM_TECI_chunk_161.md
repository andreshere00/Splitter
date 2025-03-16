Augmentation

Top-k documents are combined with the input text to enrich the context of the gen-
erator model. In the original paper, this information is concatenated. For every retrieved
document, a new query is generated, providing the model with enough domain-specific
knowledge to answer the original input query:

xa = {x||zk

1, . . . , x||zk
k}

(4.4)

Generator