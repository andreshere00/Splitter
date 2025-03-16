ˆE = MT(F ),

(B.1)

which returns a translation estimation ˆE given a source sentence F as input. So, SMT
systems perform machine translation tasks based on a Bayesian inference: the probability
of E given F is given by the expression P (E | F ; θ).

Then, training the model aims to find a target sentence that maximizes the probability:

ˆE = arg max

P (E | F ; θ)

E

(B.2)