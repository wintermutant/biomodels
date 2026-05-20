import os
import pytest
from dotenv import load_dotenv
from sqlmodel import SQLModel

import biomodels.app as app_module


@pytest.fixture(scope="session", autouse=True)
def test_database():
    """Point the engine at genomics_test and create all tables fresh."""
    load_dotenv(".env.test", override=True)
    app_module._engine = None  # force re-initialization from .env.test
    engine = app_module.get_engine()
    SQLModel.metadata.drop_all(engine)
    SQLModel.metadata.create_all(engine)
    yield
    SQLModel.metadata.drop_all(engine)


@pytest.fixture
def data_key():
    class Record:
        def __init__(self, header, sequence):
            self.header = header
            self.sequence = sequence

    return {
        1: Record("seq1", "ATGC"),
        2: Record("seq2", "GGTC"),
        3: Record("seq3", "ATGC"),  # duplicate of seq1
    }
