from typing import Protocol, runtime_checkable


@runtime_checkable
class FastaRecordProtocol(Protocol):
    """Interface contract for a parsed FASTA entry.

    Any object with header and sequence satisfies this — no import needed.
    """
    header: str
    sequence: str
