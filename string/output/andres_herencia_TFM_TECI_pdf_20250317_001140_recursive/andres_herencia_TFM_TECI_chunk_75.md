Since the input is usually a sentence, represented by vectors, from now on forward
input will be considered as xt = (x1, x2, . . . , xN), meanwhile the output will be yt =
(y1, y2, . . . , yM).

2.3.1 Output computation

If the encoder block output is denoted as RNN(e)(·), and the decoder output is denoted
as RNN(d)(·), then the model can be expressed in the following terms [43]:

• Encoder output: corresponds to the last hidden state of the encoder, computed

by the expression: