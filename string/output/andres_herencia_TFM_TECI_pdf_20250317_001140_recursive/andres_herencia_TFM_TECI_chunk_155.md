Architecture

RAG system comprises a retriever block and a generative model (such as a Transformer).
The first block, the retriever, classifies documents based on the input’s relevance and ex-
tracts the top- k most related documents. In the augmentation phase, input and document
texts are combined to give new context to the generative model’s prompt. Finally, the
generative model (a LLM with encoder-decoder structure) generates the output. Observe
Figure 4.2.