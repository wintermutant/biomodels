import logging
from typing import Any

from sqlmodel import Session, select

from biomodels.app import get_engine
from biomodels.models import FastaEntry, FastaFile, Sequence, compute_sequence_hash
from biomodels.schemas import FastaRecordProtocol

LOGGER = logging.getLogger(__name__)


def _get_or_create_sequence(session: Session, sequence: str) -> tuple[Sequence, bool]:
    seq_hash = compute_sequence_hash(sequence)
    existing = session.exec(
        select(Sequence).where(Sequence.sequence_hash == seq_hash)
    ).first()
    if existing:
        return existing, False
    seq = Sequence(sequence=sequence)
    session.add(seq)
    session.flush()
    return seq, True


def ingest_fasta_records(
    filename: str,
    data_key: dict[int, FastaRecordProtocol],
    file_metadata: dict[str, Any] | None = None,
    engine=None,
) -> dict:
    """Ingest a data_key into the DB, deduplicating sequences.

    Accepts any dict[int, FastaRecordProtocol] — no biotools import needed.
    Returns a summary dict with counts.
    """
    eng = engine or get_engine()
    created_sequences = 0
    reused_sequences = 0

    with Session(eng) as session:
        fasta_file = FastaFile(filename=filename, file_metadata=file_metadata)
        session.add(fasta_file)
        session.flush()
        fasta_file_id = fasta_file.id

        for index, record in data_key.items():
            seq, created = _get_or_create_sequence(session, record.sequence)
            if created:
                created_sequences += 1
            else:
                reused_sequences += 1
            session.add(FastaEntry(
                file_id=fasta_file_id,
                sequence_id=seq.id,
                header=record.header,
                entry_index=index,
            ))

        session.commit()
        LOGGER.info("Ingested %d entries from %s (%d new, %d reused sequences)",
                    len(data_key), filename, created_sequences, reused_sequences)

    return {
        'file_id': fasta_file_id,
        'entries': len(data_key),
        'sequences_created': created_sequences,
        'sequences_reused': reused_sequences,
    }
