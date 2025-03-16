This metric quantifies the matched number of tokens (previously semantically grouped
using lemmatization techniques) in target PMETEOR or reference RMETEOR sequences over
the total number of tokens in those sequences. Then, the harmonic mean FMETEOR is
calculated:

PMETEOR =

RMETEOR =

FMETEOR =

Number of matched tokens
Total tokens in candidate
Number of matched tokens
Total tokens in reference
α · P · R
R + β · P

(5.5)

(5.6)

(5.7)