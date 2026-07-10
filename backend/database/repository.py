from __future__ import annotations

import logging
from datetime import datetime
from typing import Optional

from .db import db
from .models import (
    Order,
    Position,
    Trade,
    Signal,
    Account,
)

logger = logging.getLogger(__name__)


# ==========================================================
# ORDER
# ==========================================================

class OrderRepository:

    def create(
        self,
        symbol: str,
        action: str,
        volume: float,
        sl: float = 0,
        tp: float = 0,
        magic: int = 777001,
        comment: str = "GoldBot"
    ) -> Order:

        order = Order(
            symbol=symbol,
            action=action,
            volume=volume,
            sl=sl,
            tp=tp,
            magic=magic,
            comment=comment,
            status="PENDING"
        )

        with db.session() as session:

            session.add(order)

            session.flush()

            session.refresh(order)

            return order

    def get_next(self) -> Optional[Order]:

        with db.session() as session:

            order = (
                session.query(Order)
                .filter(Order.status == "PENDING")
                .order_by(Order.id.asc())
                .first()
            )

            if order is None:
                return None

            order.status = "PROCESSING"
            order.processed_at = datetime.utcnow()

            session.flush()
            session.refresh(order)

            return order

    def complete(
        self,
        order_id: int,
        ticket: Optional[int] = None
    ) -> Optional[Order]:

        with db.session() as session:

            order = (
                session.query(Order)
                .filter(Order.id == order_id)
                .first()
            )

            if order is None:
                return None

            order.status = "EXECUTED"
            order.ticket = ticket
            order.processed_at = datetime.utcnow()

            session.flush()
            session.refresh(order)

            return order

    def failed(
        self,
        order_id: int,
        error: str
    ) -> Optional[Order]:

        with db.session() as session:

            order = (
                session.query(Order)
                .filter(Order.id == order_id)
                .first()
            )

            if order is None:
                return None

            order.status = "FAILED"
            order.error = error
            order.processed_at = datetime.utcnow()

            session.flush()
            session.refresh(order)

            return order


order_repository = OrderRepository()


# ==========================================================
# POSITION
# ==========================================================

class PositionRepository:

    def upsert(
        self,
        ticket: int,
        symbol: str,
        position_type: str,
        volume: float,
        price_open: float,
        price_current: float,
        sl: float,
        tp: float,
        profit: float,
        swap: float,
        commission: float,
        magic: int,
        comment: str,
    ) -> Position:

        with db.session() as session:

            position = (
                session.query(Position)
                .filter(Position.ticket == ticket)
                .first()
            )

            if position is None:

                position = Position(
                    ticket=ticket,
                    symbol=symbol,
                    type=position_type,
                    volume=volume,
                    price_open=price_open,
                    price_current=price_current,
                    sl=sl,
                    tp=tp,
                    profit=profit,
                    swap=swap,
                    commission=commission,
                    magic=magic,
                    comment=comment,
                    status="OPEN",
                )

                session.add(position)

            else:

                position.symbol = symbol
                position.type = position_type
                position.volume = volume
                position.price_open = price_open
                position.price_current = price_current
                position.sl = sl
                position.tp = tp
                position.profit = profit
                position.swap = swap
                position.commission = commission
                position.magic = magic
                position.comment = comment
                position.status = "OPEN"
                position.updated_at = datetime.utcnow()

            session.flush()
            session.refresh(position)

            return position

    def get_all(self):

        with db.session() as session:

            return (
                session.query(Position)
                .order_by(Position.ticket)
                .all()
            )

    def get_open(self):

        with db.session() as session:

            return (
                session.query(Position)
                .filter(Position.status == "OPEN")
                .all()
            )

    def close(self, ticket: int):

        with db.session() as session:

            position = (
                session.query(Position)
                .filter(Position.ticket == ticket)
                .first()
            )

            if position is None:
                return None

            position.status = "CLOSED"
            position.updated_at = datetime.utcnow()

            session.flush()
            session.refresh(position)

            return position


position_repository = PositionRepository()


# ==========================================================
# TRADE
# ==========================================================

class TradeRepository:

    def create(
        self,
        ticket: int,
        symbol: str,
        action: str,
        volume: float,
        entry_price: float
    ):

        trade = Trade(
            ticket=ticket,
            symbol=symbol,
            action=action,
            volume=volume,
            entry_price=entry_price,
        )

        with db.session() as session:

            session.add(trade)

            session.flush()

            session.refresh(trade)

            return trade


trade_repository = TradeRepository()


# ==========================================================
# SIGNAL
# ==========================================================

class SignalRepository:

    def create(
        self,
        symbol: str,
        direction: str,
        strategy: str,
        confidence: float,
        note: str = ""
    ):

        signal = Signal(
            symbol=symbol,
            direction=direction,
            strategy=strategy,
            confidence=confidence,
            note=note,
        )

        with db.session() as session:

            session.add(signal)

            session.flush()

            session.refresh(signal)

            return signal


signal_repository = SignalRepository()


# ==========================================================
# ACCOUNT
# ==========================================================

class AccountRepository:

    def save(
        self,
        broker: str,
        account_number: str,
        balance: float,
        equity: float,
        margin: float,
        free_margin: float,
        currency: str,
        leverage: int,
    ):

        with db.session() as session:

            account = session.query(Account).first()

            if account is None:

                account = Account()

                session.add(account)

            account.broker = broker
            account.account_number = account_number
            account.balance = balance
            account.equity = equity
            account.margin = margin
            account.free_margin = free_margin
            account.currency = currency
            account.leverage = leverage

            session.flush()

            session.refresh(account)

            return account


account_repository = AccountRepository()