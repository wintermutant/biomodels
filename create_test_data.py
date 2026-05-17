import random

random.seed(14)

SEQUENCES = [
    {'sequence': "".join(random.choices("ATGC", k=25))}
    for _ in range(10)
]


def create_random_sequences(n: int = 10, k: int = 25, seed=12345) -> list[dict]:
    random.seed(seed)
    return [
        {'sequence': "".join(random.choices("ATGC", k=k))}
        for _ in range(n)
    ]
