2. lora_r : specifies the rank dimension r in the LoRA configuration. For a weight
matrix of Rm×n, the number of new parameters can be computed as follows: Number
of parameters = (m × r) + (r × n). When r << m or r << n the number of param-
eters decreases significantly.

3. lora_alpha: This parameter indicates the scaling factor α for the re-parameterized

weights matrix, as defined in equation 4.6.