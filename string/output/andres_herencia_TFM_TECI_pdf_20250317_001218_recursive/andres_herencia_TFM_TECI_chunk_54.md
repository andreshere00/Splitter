ezj
k=1 ezk

(cid:80)K

, for j = 1, . . . , K, being z a RK-dimensional vector.

Figure 2.2: Activation function examples.

4

2.1. NEURAL NETWORK CONCEPT

Output computation

Let x = (x1, x2, . . . , xN ) the input vector and w = (w1, w,2, . . . , wN ) the weights vector.
Then, the output can be computed as follows:

y = sgn

N
(cid:88)

i=1

wixi + b

(2.1)

The architecture diagram can be shown in Figure 2.3.

Input data
x1
x2
...

w1
w2

wN

f

y

Output data

xN

b