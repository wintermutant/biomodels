import time

from sqlmodel import Field, Session, SQLModel, create_engine

from data import SEQUENCES
import sql_models as sqlm

DB_CONNECTION = "postgresql+psycopg2://dane:deemer@localhost:5432/genomics"

engine = create_engine(
    'postgresql+psycopg2://dane:deemer@localhost:5432/genomics',
    connect_args={"application_name": "debug_connection"},
    echo=True
    )

def timelimit_connect(timelimit: int = 10):
    with engine.connect() as conn:
        print("Connected for 10 seconds...")
        time.sleep(timelimit)
        print('Done')

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def create_sequence_models(raw_sequence_data: list[dict]):
    my_models: list[sqlm.Sequence] = []
    for data in raw_sequence_data:
        my_models.append(sqlm.Sequence(**data))
    return my_models

def updata_sequence_table(my_models: list[sqlm.Sequence]):
    with Session(engine) as session:
        for model in my_models:
            session.add(model)
            session.commit()


if __name__ == "__main__":
    create_db_and_tables()
    modeled_data = create_sequence_models(SEQUENCES)
    print(f'My models:\n{modeled_data}')
    updata_sequence_table(modeled_data)
