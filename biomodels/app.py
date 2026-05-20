import logging
import os

from dotenv import load_dotenv
from sqlmodel import SQLModel, create_engine

LOGGER = logging.getLogger(__name__)

load_dotenv()

_engine = None


def _get_connection_string() -> str:
    conn = os.getenv("BIOMODELS_DB_CONNECTION")
    if not conn:
        raise RuntimeError(
            "BIOMODELS_DB_CONNECTION is not set. "
            "Add it to your .env file or environment."
        )
    LOGGER.info('Returning conection string %s', conn)
    return conn


def initialize(engine_string: str | None = None):
    """Return an engine. Uses BIOMODELS_DB_CONNECTION env var if no string given."""
    global _engine
    _engine = create_engine(
        engine_string or _get_connection_string(),
        connect_args={"application_name": "biomodels"},
        echo=False,
    )
    LOGGER.info('Returning _engine')
    return _engine


def get_engine():
    """Return the current engine, initializing from env if needed."""
    global _engine
    if _engine is None:
        _engine = initialize()
        LOGGER.debug('Engine initialized!')
    LOGGER.debug('Returning engine')
    return _engine


def create_db_and_tables():
    SQLModel.metadata.create_all(get_engine())
