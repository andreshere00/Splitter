The relative and absolute embedding generation concepts are retrieved from the original
Transformer architecture, but in this case, LLaMA combines both concepts on a single
mathematical expression. This model generates queries and keys solely based on sinusoids,
without an additive mechanism (see Figure F.1), reducing the operational complexity of
the model. [3]

In fact, RoPE states for a weighted rotation matrix when generating the queries and

key sets, as shown in the following equation: