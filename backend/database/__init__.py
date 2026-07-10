from .db import Base, db


# register models
# supaya Base.metadata mengenal semua table

from . import models


__all__ = [
    "Base",
    "db",
]