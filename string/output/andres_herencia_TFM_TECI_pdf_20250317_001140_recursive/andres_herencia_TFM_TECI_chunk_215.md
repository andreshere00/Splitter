xi∈x

max
xi∈x

x⊤
i ˆxj

max
ˆxj ∈ˆx

x⊤
i ˆxj

FBERT =2

PBERT · RBERT
PBERT + RBERT

(5.2)

(5.3)

(5.4)

Here, |x| and |ˆx| represent the number of tokens in the reference and target sequences,
respectively. Optionally, importance weighting (given by the inverse document frequency

41

5.3. EVALUATION

scores, or idf ) can be applied to different match types. These three metrics collectively
define the BERTScore. An explanation diagram for FBERT computation is provided in
Figure 5.3.