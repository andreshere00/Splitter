32

4.2. LLM CUSTOMIZATION TECHNIQUES

later implementations, a regularization term that controls the importance of the adapter’s
weight has been added, given by the α parameter. So, the final weights are given by the
following expression:

W ′ = W +

α
r

(AB)

(4.6)

(a) Adapter fine-tuning rep-
resentation.

(b) LoRA fine-tuning repre-
sentation.

Figure 4.4: Comparison of adapter-based fine-tuning techniques.