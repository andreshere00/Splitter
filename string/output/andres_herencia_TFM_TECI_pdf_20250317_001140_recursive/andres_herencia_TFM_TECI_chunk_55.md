y

Output data

xN

b

Figure 2.3: Simple perceptron architecture.

Training

In the training process, the aim is to obtain a weights vector such that all the produced
outputs (based on the supervised training set, yd = {yd
n}) are well classified.
For this purpose, a learning rule is followed, governed by a discrete-time dynamic system:
[22]

2, . . . , yd

1, yd

wt+1 = wt + η(yd − y)x

(2.2)

where η is the learning rate, a parameter that modulates the speed at which the