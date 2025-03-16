Suppose the input for the target layers is X. Let W ∈ Rn×m be the pre-trained
weights matrix. LoRA constructs matrices A and B as follows: A is initialized with
random Gaussian values, while B is initially a zero matrix, so the initial weight update
is zero, ∆W = AB = 0. During fine-tuning, the pre-trained weights W are frozen, and
new weight updates are computed via the product of the two low-rank matrices A and B.