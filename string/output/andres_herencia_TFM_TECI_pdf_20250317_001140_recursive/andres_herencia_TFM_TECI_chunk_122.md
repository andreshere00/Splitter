3.3.3 Masking technique inside attention layers

As can be seen in Figure 3.1, a masked Multi-Head Attention mechanism is used in-
stead of a vanilla one in the decoder’s attention layer block. This masking ensures that
the predictions for a particular position depend only on the known outputs at previous
positions.