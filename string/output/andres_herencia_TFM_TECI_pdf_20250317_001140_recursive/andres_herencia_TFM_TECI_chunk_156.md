Figure 4.2: An example of a Retrieval-Augmented Generation (RAG) system.

Output computation

Retriever

29

4.2. LLM CUSTOMIZATION TECHNIQUES

In the original paper, [34] the retriever was based on a a Dense Passage Retrieval

(DPR) [26] model, consisting in two encoder blocks:

• The first block encodes the query as a vector representation (embedding). This is,

given an input text x, it produces a dense vector q(x).