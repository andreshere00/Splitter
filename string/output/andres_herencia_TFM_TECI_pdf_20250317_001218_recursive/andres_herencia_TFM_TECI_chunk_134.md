Despite LLaMA being based on the Transformer architecture, it does not have an
encoder-decoder architecture. Due to the model is intended to be used for text generation
tasks, the encoder block has been omitted. However, some implementations use BERT
encoder models along with LLaMA decoders (e.g., RAG, see section 4.2.2, providing a
larger context window for tasks such as summarization or translation.

23

3.7. LLAMA ARCHITECTURE