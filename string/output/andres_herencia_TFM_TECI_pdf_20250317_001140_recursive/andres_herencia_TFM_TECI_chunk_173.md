When using Low Rank Adapters, low-rank decomposition matrices are attached to
reparameterize the existing weight matrices. Instead of adding new layers to the model,
LoRA introduces two low-rank matrices that modify the existing weights by adding their
product as an update [23]. This method maintains the original layer structure and relies
on matrix (tensor) computations, making LoRA faster and more efficient than traditional
adapter methods (Figure 4.4b).