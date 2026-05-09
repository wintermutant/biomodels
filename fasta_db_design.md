# FASTA Database Design, Constraints, and Sequence Analytics

## Overview

This document summarizes a scalable architecture for storing,
deduplicating, and analyzing FASTA sequence data using: - PostgreSQL
relational schema - SQLAlchemy ORM models - Pydantic validation layer -
k-mer analytics and constraint modeling

------------------------------------------------------------------------

# Core Design Goals

-   Store FASTA files without duplicating sequences
-   Preserve exact file reconstruction capability
-   Optimize for fast reads (GET-heavy workload)
-   Enable biological analytics (k-mers, motifs, constraints)
-   Support scalable ingestion pipelines

------------------------------------------------------------------------

# Database Schema

## sequence (deduplicated content)

Stores unique biological sequences only.

``` sql
sequence
--------
id (PK)
sequence (TEXT)
sequence_hash (UNIQUE, INDEX)
```

------------------------------------------------------------------------

## fasta_file (file metadata)

``` sql
fasta_file
----------
id (PK)
filename
metadata (JSONB)
```

------------------------------------------------------------------------

## fasta_entry (core observational table)

Represents a sequence occurrence within a file.

``` sql
fasta_entry
------------
id (PK)
file_id (FK → fasta_file)
sequence_id (FK → sequence)
header (TEXT)
entry_index (INT)
```

Key properties: - One row per file-specific occurrence - Preserves
ordering - Enables full reconstruction

------------------------------------------------------------------------

## Reconstruction Query

``` sql
SELECT e.header, s.sequence
FROM fasta_entry e
JOIN sequence s ON e.sequence_id = s.id
WHERE e.file_id = :file_id
ORDER BY e.entry_index;
```

------------------------------------------------------------------------

# Why This Design Works

-   sequence = global deduplicated biology
-   fasta_entry = file context + ordering
-   fasta_file = dataset metadata

fasta_entry is expected to be the largest table.

------------------------------------------------------------------------

# Constraint Engine

A learned rule system derived from sequence statistics.

Example: - A → G never occurs

``` python
constraints = {
    "A": {"A", "T", "C"}
}
```

Benefits: - Prunes invalid search space - Speeds validation and motif
search - Encodes biological structure

------------------------------------------------------------------------

# k-mer Signature Indexing

## Table

``` sql
kmer_index
----------
kmer
sequence_id
```

## Query

``` sql
SELECT sequence_id
FROM kmer_index
WHERE kmer = 'AAT';
```

Benefits: - Replaces expensive substring scans - Enables fast motif
lookup - Acts as inverted index

------------------------------------------------------------------------

# Transition Model (Markov-style)

``` sql
transition
----------
prefix
next_base
count
```

Used to: - Learn base transition probabilities - Detect impossible
transitions - Build constraint engine

------------------------------------------------------------------------

# Motif Table

``` sql
motif
------
pattern
length
support
score
```

Stores biologically significant patterns: - enriched k-mers - conserved
motifs - signatures

------------------------------------------------------------------------

# Sequence as k-mer Vector

Example sequence: ATGCAAT

k=2 representation:

  kmer   count
  ------ -------
  AA     1
  AT     2
  TG     1
  GC     1
  CA     1

Uses: - similarity search - clustering - anomaly detection

------------------------------------------------------------------------

# SQLAlchemy Models

``` python
class Sequence(Base):
    __tablename__ = "sequence"
    id = Column(Integer, primary_key=True)
    sequence = Column(Text)
    sequence_hash = Column(String, unique=True, index=True)


class FastaFile(Base):
    __tablename__ = "fasta_file"
    id = Column(Integer, primary_key=True)
    filename = Column(Text)
    metadata = Column(Text)


class FastaEntry(Base):
    __tablename__ = "fasta_entry"
    id = Column(Integer, primary_key=True)
    file_id = Column(Integer, ForeignKey("fasta_file.id"))
    sequence_id = Column(Integer, ForeignKey("sequence.id"))
    header = Column(Text)
    entry_index = Column(Integer)
```

------------------------------------------------------------------------

# Pydantic Models (Validation Layer)

``` python
class FastaRecord(BaseModel):
    header: str
    sequence: str

    def sequence_hash(self):
        import hashlib
        return hashlib.sha256(self.sequence.encode()).hexdigest()


class FileMetadata(BaseModel):
    model_config = {"extra": "allow"}
    organism: str | None = None
```

------------------------------------------------------------------------

# Ingestion Pipeline (Pseudocode)

``` python
def ingest_fasta(session, file_path):
    file = FastaFile(filename=file_path)
    session.add(file)
    session.flush()

    for i, record in enumerate(stream_fasta(file_path)):
        seq = get_or_create_sequence(record.sequence)

        entry = FastaEntry(
            file_id=file.id,
            sequence_id=seq.id,
            header=record.header,
            entry_index=i
        )

        session.add(entry)

    session.commit()
```

------------------------------------------------------------------------

# Analytics Pipeline

## k-mer computation

``` python
for sequence in sequences:
    for i in range(len(sequence)-k+1):
        kmer = sequence[i:i+k]
        increment_kmer(kmer)
```

## Transition analysis

``` python
for sequence in sequences:
    for i in range(len(sequence)-1):
        update_transition(sequence[i], sequence[i+1])
```

------------------------------------------------------------------------

# Architecture Summary

  Layer             Responsibility
  ----------------- -----------------------------
  Pydantic          Validation + parsing
  SQLAlchemy        Relational structure
  PostgreSQL        Storage + indexing
  Analytics layer   k-mers, motifs, constraints

------------------------------------------------------------------------

# Key Insight

This system evolves from:

> FASTA storage system

to:

> Learned, queryable biological sequence model
