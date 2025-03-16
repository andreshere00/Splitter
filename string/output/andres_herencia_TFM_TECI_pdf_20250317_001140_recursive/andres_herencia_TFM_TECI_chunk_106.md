Even if coding each position with a method such as one-hot is possible, it cannot
capture the distance between each element of a sequence, i.e., its relative position. So,
the aim of position encoding is not only to represent its absolute position (the word
position in the entire text) but also the relative position (the position in the sentence).
For this purpose, a sinusoidal-based encoding method is proposed: [61]

P E(pos,2i) = sin

(cid:18)

P E(pos,2i+1) = cos