i , y1:i−1)

(4.5)

The final output sequence is obtained by marginalizing the probabilities from the differ-
ent retrieved documents, ensuring that the generated text is contextually relevant and
accurate based on the augmented input. In the original paper, the generator used was a
BART, but it could be any encoder-decoder architecture. [34]

4.2.3 Fine-tuning

Transfer Learning (TL)