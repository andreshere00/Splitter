Although fine-tuning allows the model to adapt well to the new task, it has two disad-
vantages: catastrophic forgetting and high computational cost. Catastrophic forgetting
occurs when an ANN forgets previously learned information while acquiring new knowl-
edge in the re-training phase [30]. To mitigate catastrophic forgetting, it is convenient to
freeze an important fraction of the top layers. On the other hand, fine-tuning requires
substantial hardware computational resources.