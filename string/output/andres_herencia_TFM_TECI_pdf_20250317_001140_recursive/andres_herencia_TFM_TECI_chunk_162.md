(4.4)

Generator

The generator takes the augmented input xa and generates the output sequence. For
in the top-k set, the generator produces a probability distribution over

each document zk
i

30

4.2. LLM CUSTOMIZATION TECHNIQUES
the next token yi:

pθ(yi|x, zk

i , y1:i−1)

(4.5)