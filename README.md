# biomodels

Database models and ingestion connectors for bioinformatics data types.

Part of a broader ecosystem of decoupled libraries:
- **caragols** — CLI framework, config management, reporting
- **biotools** — bioinformatics file processing (FASTA, VCF, etc.)
- **biomodels** — ORM models and DB ingestion (this package)
- **bioserver** — API service built on biotools + biomodels
- **biocompute** — SLURM/HPC connectivity

---

## Setup

Create a `.env` file in your project root (or export to your shell):

```
BIOMODELS_DB_CONNECTION=postgresql+psycopg2://user:password@localhost:5432/yourdb
```

Install:

```bash
uv pip install -e .
```

---

## Connecting an external library

biomodels uses **structural subtyping (Protocols)** to define its ingestion contracts.
You do not need to import from biomodels to satisfy them — you just need objects with the right shape.

### FASTA example

biomodels expects `dict[int, FastaRecordProtocol]` where each value has:

```python
header: str
sequence: str
```

Any object satisfying that shape works — dataclass, Pydantic model, plain class:

```python
from dataclasses import dataclass

@dataclass
class MyFastaRecord:
    header: str
    sequence: str
```

Then ingest:

```python
from biomodels.app import create_db_and_tables
from biomodels.db_connectors import db_connection
from biomodels.db_connectors.fasta import ingest_fasta_records

create_db_and_tables()

data_key = {
    1: MyFastaRecord(header="seq1", sequence="ATGC"),
    2: MyFastaRecord(header="seq2", sequence="GGTC"),
}

summary = ingest_fasta_records(filename="myfile.fasta", data_key=data_key)
# {'file_id': 1, 'entries': 2, 'sequences_created': 2, 'sequences_reused': 0}
```

Sequences are **automatically deduplicated** — if the same sequence already exists in the DB
it is reused rather than duplicated.

### Adding a new file type (e.g. VCF)

1. Add a Protocol to `biomodels/schemas.py`:

```python
class VcfRecordProtocol(Protocol):
    chrom: str
    pos: int
    ref: str
    alt: str
    qual: float | None
```

2. Add a connector at `biomodels/db_connectors/vcf.py` with `ingest_vcf_records(filename, data_key, ...)`.
3. Add the corresponding SQLModel tables to `biomodels/models.py`.

No changes needed in the calling library.

---

## Schema

```
sequence        — deduplicated biological sequences (one row per unique sequence)
fasta_file      — one row per ingested file, with JSONB metadata
fasta_entry     — one row per header/sequence occurrence; FK to both tables
```

Reconstruction query:

```sql
SELECT e.header, s.sequence
FROM fasta_entry e
JOIN sequence s ON e.sequence_id = s.id
WHERE e.file_id = :file_id
ORDER BY e.entry_index;
```

---

## Design principles

- **biomodels owns the DB layer only** — no file parsing, no CLI, no stats
- **biotools (or any library) owns parsing** — produces the shape biomodels expects, nothing more
- **Protocols over inheritance** — calling libraries satisfy contracts implicitly, no biomodels import required at parse time
- **Sequence deduplication by default** — the same sequence across many files is stored once
