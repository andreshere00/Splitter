42

5.4. WORKFLOW

where chunks refers to the number of consecutive token matches, and θ and γ are con-
figurable parameters. The final METEOR score combines the penalty term with the
harmonic mean as follows:

METEOR = FMETEOR · (1 − Penalty)

(5.9)

Consider the previous example with the same reference and target sentences. Since both
sentences are formulated in different order and length, this score is not as high as the
obtained in the BERT Score metric: 0.24390244.

5.4 Workflow