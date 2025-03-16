Let V be a finite set defining the vocabulary, consisting of a set of tokens. A token is a
unit that divides a text into blocks, usually represented by a word, a letter, or a sub-word
(see Appendix E.3). Let x be a sequence of tokens x = (x1, x2, . . . , xN ), where x ∈ V ∗.
Then, an embedding can be expressed as a token representation in an Rn-dimensional
space, i.e., f : V → Rn. In the specific context of Transformers, embeddings have the
same dimension as the model, n = d = 512 [48].