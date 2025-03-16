Similarly to the LSTM, the Gated Recurrent Unit (GRU) architecture integrates mech-
anisms to control the information flow. However, it simplifies the model by combining
the input and forget gates into a single update gate, and merging the cell state with the
hidden state. [10]

Figure D.1: GRU cell. [15]

The GRU are composed by the following elements (see Figure D.1):

• Update Gate:

zt = σ(WHZ · ht−1 + WXZ · xt + bz)

(D.1)