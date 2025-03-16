• The encoder vector is the final hidden state produced by the encoder. This
vector aims to encapsulate the information for all input elements in order to help
the decoder make accurate predictions.

• The decoder is a stack of M recurrent units where each predicts an output yt at a
time step t. Each recurrent unit accepts a hidden state from the previous unit and
produces an output and a hidden state.