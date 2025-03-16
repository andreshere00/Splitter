The input for the feed-forward layers is processed in two ways: as the input of the GLU,
and to project input into a higher-dimension vector space. In contrast, ReLU function
only performs this second operation (see Figure 3.6. [55]

24

3.7. LLAMA ARCHITECTURE

Figure 3.6: SwiGLU feed.forward layers vs vanilla feed-forward layers. “fc” responds to
fully connected. [14]

The mathematical expression of this function can be described as follows: