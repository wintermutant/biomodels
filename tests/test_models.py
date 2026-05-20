from biomodels.models import Sequence, compute_sequence_hash, normalize_sequence


def test_sequence_hash_set_on_create():
    seq = Sequence(sequence="ATGC")
    assert seq.sequence_hash == compute_sequence_hash("ATGC")


def test_sequence_normalization_lowercase():
    assert normalize_sequence("atgc") == "ATGC"


def test_sequence_normalization_whitespace():
    assert normalize_sequence("  AT GC  ") == "ATGC"


def test_sequence_hash_consistent():
    assert compute_sequence_hash("ATGC") == compute_sequence_hash("atgc")
    assert compute_sequence_hash("ATGC") == compute_sequence_hash("  AT GC  ")
