(cid:19)

(3.1)

Where pos ∈ {1, 2, . . . , k} is the position of the input token and i ∈ {0, 1, . . . , d − 1}
is the index of each element in the pos encoding vector. This is, for an even index
inside the pos-th encoding vector, a sine is employed, and for an odd position, a cosine.
The wavelengths form a geometric progression from 2π to 10000 · 2π. 10,000 is used as
the denominator base following empirical results. A more deep approach to positional
embedding can be found in Appendix F).