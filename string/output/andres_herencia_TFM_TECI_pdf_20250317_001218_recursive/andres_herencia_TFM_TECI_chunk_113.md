The attention function for a query set (matrix) Q and a key set K will be denoted as
f (Q, K). Generally, this function is computed matrix-wise, and not vector or component-
wise. These are some famous examples: [44]

• Additive: f (Q, K) = softmax(WKK T + WQQT + b). Note that this expression can

be implemented with a FNN.

• Multiplicative (dot-product): f (Q, K) = softmax (cid:0)QK T (cid:1).

• Scaled dot-product: f (Q, K) = softmax( QKT
dk
• General attention: f (Q, K) = softmax(QW T
V K)