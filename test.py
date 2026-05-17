from sqlmodel import Session

from data import create_random_sequences
from main import engine
import models


def create_sequence_models(raw_sequence_data: list[dict]):
    my_models: list[models.Sequence] = []
    for data in raw_sequence_data:
        my_models.append(models.Sequence(**data))
    return my_models


def updata_sequence_table(my_models: list[models.Sequence]):
    with Session(engine) as session:
        for model in my_models:
            session.add(model)
            session.commit()


def test_add_new_sequences(n=10, k=25, seed=1234) -> bool:
    sequences = create_random_sequences(n, k, seed)
    test_models = create_sequence_models(sequences)
    updata_sequence_table(test_models)
    return True


if __name__ == "__main__":
    test_add_new_sequences()