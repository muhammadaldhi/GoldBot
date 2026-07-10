from __future__ import annotations

from datetime import datetime
from typing import Optional

from sqlalchemy import (
    DateTime,
    Integer,
    Numeric,
    String,
    Text,
)
from sqlalchemy.orm import Mapped, mapped_column

from .db import Base


# =========================
# Account Model
# =========================

class Account(Base):
    """
    Menyimpan informasi akun trading.
    """

    __tablename__ = "accounts"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True
    )

    broker: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    account_number: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    balance: Mapped[float] = mapped_column(
        Numeric(12, 2),
        default=0
    )

    equity: Mapped[float] = mapped_column(
        Numeric(12, 2),
        default=0
    )

    currency: Mapped[str] = mapped_column(
        String(10),
        default="USD"
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow
    )


# =========================
# Trade Model
# =========================

class Trade(Base):
    """
    Menyimpan history transaksi trading.
    """

    __tablename__ = "trades"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True
    )

    symbol: Mapped[str] = mapped_column(
        String(20),
        nullable=False
    )

    action: Mapped[str] = mapped_column(
        String(10),
        nullable=False
    )
    # BUY / SELL


    lot: Mapped[float] = mapped_column(
        Numeric(8, 2),
        default=0
    )

    entry_price: Mapped[float] = mapped_column(
        Numeric(12, 5),
        nullable=True
    )

    exit_price: Mapped[float] = mapped_column(
        Numeric(12, 5),
        nullable=True
    )

    profit_loss: Mapped[float] = mapped_column(
        Numeric(12, 2),
        default=0
    )

    status: Mapped[str] = mapped_column(
        String(20),
        default="OPEN"
    )
    # OPEN / CLOSED


    opened_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow
    )

    closed_at: Mapped[Optional[datetime]] = mapped_column(
    DateTime,
    nullable=True
)


# =========================
# Signal Model
# =========================

class Signal(Base):
    """
    Menyimpan hasil analisa bot.
    """

    __tablename__ = "signals"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True
    )

    symbol: Mapped[str] = mapped_column(
        String(20),
        nullable=False
    )

    direction: Mapped[str] = mapped_column(
        String(10),
        nullable=False
    )
    # BUY / SELL


    strategy: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    confidence: Mapped[float] = mapped_column(
        Numeric(5, 2),
        default=0
    )

    note: Mapped[Optional[str]] = mapped_column(
    Text,
    nullable=True
)

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow
    )