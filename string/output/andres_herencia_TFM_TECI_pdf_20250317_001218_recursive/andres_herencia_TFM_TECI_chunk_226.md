In all the experiments, LoRA was applied exclusively to the attention layers. As
observed, only the query and value components of the attention mechanism are fine-tuned.
The query matrix is retrained due to its critical role in learning the new dataset’s queries.
The value matrix captures the new relationships with the query, forming a revised context
for the model. Training additional layers can lead to catastrophic forgetting problems due