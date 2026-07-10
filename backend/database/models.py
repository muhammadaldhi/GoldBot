from __future__ import annotations

from datetime import datetime
from typing import Optional

from sqlalchemy import (
    DateTime,
    Float,
    Integer,
    String,
    Text,
)

from sqlalchemy.orm import (
    Mapped,
    mapped_column,
)

from .db import Base


# ==========================================================
# ORDER
# ==========================================================

class Order(Base):

    __tablename__ = "orders"

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

    volume: Mapped[float] = mapped_column(
        Float,
        nullable=False
    )

    sl: Mapped[float] = mapped_column(
        Float,
        default=0
    )

    tp: Mapped[float] = mapped_column(
        Float,
        default=0
    )

    magic: Mapped[int] = mapped_column(
        Integer,
        default=777001
    )

    comment: Mapped[str] = mapped_column(
        String(100),
        default="GoldBot"
    )

    status: Mapped[str] = mapped_column(
        String(20),
        default="PENDING"
    )

    ticket: Mapped[Optional[int]] = mapped_column(
        Integer,
        nullable=True
    )

    error: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow
    )

    processed_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime,
        nullable=True
    )


# ==========================================================
# POSITION
# ==========================================================

class Position(Base):

    __tablename__ = "positions"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True
    )

    ticket: Mapped[int] = mapped_column(
        Integer,
        unique=True
    )

    symbol: Mapped[str] = mapped_column(
        String(20)
    )

    type: Mapped[str] = mapped_column(
        String(10)
    )

    volume: Mapped[float] = mapped_column(
        Float
    )

    price_open: Mapped[float] = mapped_column(
        Float
    )

    price_current: Mapped[float] = mapped_column(
        Float,
        default=0
    )

    sl: Mapped[float] = mapped_column(
        Float,
        default=0
    )

    tp: Mapped[float] = mapped_column(
        Float,
        default=0
    )

    profit: Mapped[float] = mapped_column(
        Float,
        default=0
    )

    swap: Mapped[float] = mapped_column(
        Float,
        default=0
    )

    commission: Mapped[float] = mapped_column(
        Float,
        default=0
    )

    magic: Mapped[int] = mapped_column(
        Integer,
        default=777001
    )

    comment: Mapped[str] = mapped_column(
        String(100),
        default=""
    )

    status: Mapped[str] = mapped_column(
        String(20),
        default="OPEN"
    )

    opened_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )


# ==========================================================
# TRADE HISTORY
# ==========================================================

class Trade(Base):

    __tablename__ = "trades"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True
    )

    ticket: Mapped[int] = mapped_column(
        Integer
    )

    symbol: Mapped[str] = mapped_column(
        String(20)
    )

    action: Mapped[str] = mapped_column(
        String(10)
    )

    volume: Mapped[float] = mapped_column(
        Float
    )

    entry_price: Mapped[float] = mapped_column(
        Float
    )

    exit_price: Mapped[Optional[float]] = mapped_column(
        Float,
        nullable=True
    )

    profit: Mapped[float] = mapped_column(
        Float,
        default=0
    )

    opened_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow
    )

    closed_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime,
        nullable=True
    )


# ==========================================================
# SIGNAL
# ==========================================================

class Signal(Base):

    __tablename__ = "signals"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True
    )

    symbol: Mapped[str] = mapped_column(
        String(20)
    )

    direction: Mapped[str] = mapped_column(
        String(10)
    )

    strategy: Mapped[str] = mapped_column(
        String(100)
    )

    confidence: Mapped[float] = mapped_column(
        Float
    )

    note: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow
    )


# ==========================================================
# ACCOUNT
# ==========================================================

class Account(Base):

    __tablename__ = "accounts"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True
    )

    broker: Mapped[str] = mapped_column(
        String(100)
    )

    account_number: Mapped[str] = mapped_column(
        String(100)
    )

    balance: Mapped[float] = mapped_column(
        Float,
        default=0
    )

    equity: Mapped[float] = mapped_column(
        Float,
        default=0
    )

    margin: Mapped[float] = mapped_column(
        Float,
        default=0
    )

    free_margin: Mapped[float] = mapped_column(
        Float,
        default=0
    )

    currency: Mapped[str] = mapped_column(
        String(10),
        default="USD"
    )

    leverage: Mapped[int] = mapped_column(
        Integer,
        default=100
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )