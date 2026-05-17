import logging

from sqlalchemy import text
from sqlmodel import Session

from biomodels.app import get_engine

LOGGER = logging.getLogger(__name__)


def db_connection() -> bool:
    """Return True if the DB is reachable, False otherwise."""
    try:
        with Session(get_engine()) as session:
            session.exec(text("SELECT 1"))
        return True
    except Exception as e:
        LOGGER.error("DB connection failed: %s", e)
        return False
