• The first linear transformation L1(s) = W1s + b1 abstracts the data to a higher-
dimensional vector space, allowing to capture more complex patterns about each
word and position. When the ReLU function (ReLU(s) = max (0, s)) is applied
to this expression, it prevents the gradient descent problem by replacing negative
values with zero.

• The second linear transformation L2(s) = L1W2 + b2 returns the output of the first

expression back to the required output dimension.