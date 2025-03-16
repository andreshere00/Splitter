For each discrete time interval t, the system has a hidden state ht. The hidden state
ht = (h1, h2, . . . , hM ), consists of M hidden units which represents the vector of all a(l)
terms of the hidden layers for the time step t. Thus, the system is fed back with each of the
previous and subsequent states, in addition to all inputs. The vector y = (y1, y2, . . . , yP )
[56] is produced as output. Observe Figure 2.5.

Figure 2.5: RNN architecture. [56]

2.2.1 Output computation