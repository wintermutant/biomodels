from sqlmodel import select, Session
from biomodels.app import create_db_and_tables, get_engine
from biomodels.db_connectors.fasta import ingest_fasta_records
from biomodels.models import FastaFile


def test_ingest_summary(data_key):
    create_db_and_tables()
    summary = ingest_fasta_records(filename="test.fasta", data_key=data_key)

    assert summary["entries"] == 3
    assert summary["sequences_created"] + summary["sequences_reused"] == 3
    assert summary["sequences_reused"] >= 1  # seq1 and seq3 are the same sequence


def test_ingest_fasta_file_row_exists(data_key):
    create_db_and_tables()
    summary = ingest_fasta_records(filename="test.fasta", data_key=data_key)

    with Session(get_engine()) as session:
        fasta_file = session.exec(select(FastaFile).where(FastaFile.id == summary["file_id"])).first()
    assert fasta_file is not None
    assert fasta_file.filename == "test.fasta"


def test_ingest_deduplication(data_key):
    create_db_and_tables()
    first = ingest_fasta_records(filename="run1.fasta", data_key=data_key)
    second = ingest_fasta_records(filename="run2.fasta", data_key=data_key)

    assert second["sequences_reused"] == first["sequences_created"] + first["sequences_reused"]


def test_ingest_metadata(data_key):
    create_db_and_tables()
    metadata = {"source": "lab1", "date": "2026-05-19"}
    summary = ingest_fasta_records(filename="test.fasta", data_key=data_key, file_metadata=metadata)

    with Session(get_engine()) as session:
        fasta_file = session.exec(select(FastaFile).where(FastaFile.id == summary["file_id"])).first()
    assert fasta_file.file_metadata == metadata
