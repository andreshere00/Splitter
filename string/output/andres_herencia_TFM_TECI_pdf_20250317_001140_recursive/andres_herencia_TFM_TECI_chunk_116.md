While the multiplicative mechanism is computationally more efficient than the addi-
tive one during training, it faces scaling problems as the model dimension d grows. As the
results of the dot product accumulate, the inputs to the softmax function become exces-
sively large, leading to the gradient explosion problem aforementioned (see section 2.2).
Introducing a regularization term helps alleviate this issue. Consequently, the original
paper [61] employs the scaled dot-product approach.