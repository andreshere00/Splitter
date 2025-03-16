The original LLaMA 2 architecture has been trained using Big Data from many different
sources. [58] This data has been transformed into specific formats based on the specific
task, which can be consulted on GitHub2.

2https://github.com/mallorbc/llama_dataset_formats/tree/main

37

5.2. TRAINING PROCESS

Since the fine-tuning model is intended to be used as a conversational tool, data has

been transformed into the following format:

Listing 5.1: Dataset format