'''
The scope of this is to have a database as a service. We don't want super complex logic.
Basically we just want to make the models available and allow data to be read in via:
- stream io
- pathlike object
- dictionary / in memory

As far as connecting to the engine and creating the tables (engine.create_all()), we want
this to be as simple as possible. For example, another python package might do:
from gmodels.biomodels import Sequence, Bioentry
from gmodels.app import initialize
engine = create_engine(...)
SQLModel.metadata.create_all(engine)
>>> conversely, do:
engine = initialize(engine_string="...")  # returns an engine object
mydata = Sequence(**raw_seq_dictionary)
with Session(engine) as session:
    session.add(mydata).commit()

This allows them to define their own engine or use ours boilerplate stuff. We may have a quick add:
mydata.add_and_commit()
>>> Above, this will open a session for them, add it, and commit, but not recommend

'''
import os
import time
import sys

from dotenv import load_dotenv
from sqlmodel import SQLModel, create_engine

load_dotenv()

BIOMODELS_DB_CONNECTION = os.getenv("BIOMODELS_DB_CONNECTION")
if not BIOMODELS_DB_CONNECTION:
    sys.exit('Need to set the BIOMODELS_DB_CONNECTION env variable in .env')

print(f'BIOMODELS...: {BIOMODELS_DB_CONNECTION}')


engine = create_engine(
    BIOMODELS_DB_CONNECTION,
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



if __name__ == "__main__":
    create_db_and_tables()
    # modeled_data = create_sequence_models(SEQUENCES)
    # print(f'My models:\n{modeled_data}')
    # updata_sequence_table(modeled_data)
