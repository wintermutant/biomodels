import hashlib
from datetime import datetime
from typing import Any

from sqlalchemy import Column, func
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import validates
from sqlmodel import Field, SQLModel


def normalize_sequence(sequence: str) -> str:
    return "".join(sequence.upper().split())

def compute_sequence_hash(sequence: str) -> str:
    normalized = normalize_sequence(sequence)
    return hashlib.sha256(normalized.encode("utf-8")).hexdigest()


class Sequence(SQLModel, table=True):
    __tablename__ = "sequence"

    id: int | None = Field(default=None, primary_key=True)
    sequence: str
    sequence_hash: str = Field(index=True, unique=True, nullable=False)

    @validates("sequence")
    def compute_hash(self, key, value):
        normalized = normalize_sequence(value)
        self.sequence_hash = compute_sequence_hash(normalized)
        return normalized


class FastaFile(SQLModel, table=True):
    __tablename__ = "fasta_file"

    id: int | None = Field(default=None, primary_key=True)
    filename: str
    file_metadata: dict[str, Any] | None = Field(
        default=None, sa_column=Column("metadata", JSONB)
    )
    created_at: datetime | None = Field(
        default=None, sa_column=Column("created_at", server_default=func.now(), nullable=False)
    )


class FastaEntry(SQLModel, table=True):
    __tablename__ = "fasta_entry"

    id: int | None = Field(default=None, primary_key=True)
    file_id: int = Field(foreign_key="fasta_file.id")
    sequence_id: int = Field(foreign_key="sequence.id")
    header: str
    entry_index: int
