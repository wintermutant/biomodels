from sqlmodel import Field, SQLModel
from sqlalchemy.orm import validates
import hashlib


class Sequence(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    sequence: str
    sequence_hash: str = Field(
        index=True,
        unique=True,
        nullable=False
    )
    @validates("sequence")
    def compute_hash(self, key, value):
        normalized = "".join(value.upper().split())
        self.sequence_hash = hashlib.sha256(
            normalized.encode("utf-8")

        ).hexdigest()

        return normalized
