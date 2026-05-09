import random

random.seed(13)

SEQUENCES = [
    {'sequence': "".join(random.choices("ATGC", k=25))}
    for _ in range(10)
]