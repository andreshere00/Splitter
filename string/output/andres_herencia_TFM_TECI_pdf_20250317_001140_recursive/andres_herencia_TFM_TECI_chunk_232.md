in the initial fine-tuning stages (even when the warm-up period finishes), indicating rapid
model adaptation to the dataset. Due to the presence of records with the same context,
the model periodically readjusts to new answers, causing fluctuations in the loss function.
This phenomenon has been presented in every experiment. The learning rate (Figure
6.1b) shows a smooth cosine-shaped decay. The gradient norm (Figure 6.1c) shows some