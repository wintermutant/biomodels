from biomodels.db_connectors import db_connection


def test_db_connection():
    assert db_connection(), "Could not reach the database — check BIOMODELS_DB_CONNECTION in .env"
