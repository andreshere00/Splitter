This architecture (also known as Sequence to Sequence (s2s) model) consists of three
parts: (i) the encoder; (ii) the encoding vector; and, (iii) the decoder. See Figure 2.6.

Figure 2.6: Sequence to Sequence (s2s) architecture for time step t.

• The encoder is composed of N Recurrent Units (RU) (i.e., RNNs, LSTM or GRU
cells) where each accepts a single element of the input sequence, collects information
for that element and propagates it forward.

9

2.3. ENCODER-DECODER ARCHITECTURE