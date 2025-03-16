(cid:18) QK T
√
dk

(cid:19)

+ M

V,

(3.5)

3.4 Position-wised feed-forward layers

Although a FNN is used for learning the parameters explained in section 3.3.2, another
FNN is used to capture more complex relationships over the input sets.

After the MHA layer, each position’s output (i.e., each word’s embedding) is fed
independently into the FNN. The process is conducted separately and identically for each
position, so, a unique feed-forward network is applied to all input data.