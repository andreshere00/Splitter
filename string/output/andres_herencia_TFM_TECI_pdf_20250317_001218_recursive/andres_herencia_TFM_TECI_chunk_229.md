During the fine-tuning, the dataset has been processed and evaluated over the test split.
The metrics are described in Table 6.3. The loss function values are similar for both
training and evaluation sets, indicating no signs of over-fitting. The training runtime (ap-
proximately 50 minutes) is ten times higher than the evaluation runtime (approximately
5 minutes), with a single epoch taking on an NVIDIA L4 hardware with 24 GB VRAM.