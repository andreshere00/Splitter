Training

This model is trained following the back-propagation rule, a LMS-based (Least Mean
Square) optimization method. The objective is no longer to properly classify every point,
but to minimize the error at the output, ridding the restriction that the outputs be binary.

Hence, a cost function is defined, typically involving the cross-entropy loss function
(for classification tasks) or the Mean Squared Error (MSE) (for regression tasks). Using
the MSE as example:

E(w) =

1
N

N
(cid:88)