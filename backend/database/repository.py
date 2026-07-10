from __future__ import annotations

import logging
from typing import Optional

from sqlalchemy.orm import Session

from .db import db
from .models import Account, Trade, Signal


logger = logging.getLogger(__name__)


class TradeRepository:

    def create(
        self,
        symbol: str,
        action: str,
        lot: float,
        entry_price: Optional[float] = None
    ) -> Trade:

        trade = Trade(
            symbol=symbol,
            action=action,
            lot=lot,
            entry_price=entry_price
        )

        with db.session() as session:
            session.add(trade)
            session.flush()
            session.refresh(trade)

        logger.info(
            f"Trade created: {action} {symbol} {lot}"
        )

        return trade


    def get_open_trades(self):
        with db.session() as session:

            return (
                session.query(Trade)
                .filter(
                    Trade.status == "OPEN"
                )
                .all()
            )


class SignalRepository:

    def create(
        self,
        symbol: str,
        direction: str,
        strategy: str,
        confidence: float,
        note: Optional[str] = None
    ) -> Signal:

        signal = Signal(
            symbol=symbol,
            direction=direction,
            strategy=strategy,
            confidence=confidence,
            note=note
        )

        with db.session() as session:
            session.add(signal)
            session.flush()
            session.refresh(signal)

        return signal


class AccountRepository:

    def create(
        self,
        broker: str,
        account_number: str
    ) -> Account:

        account = Account(
            broker=broker,
            account_number=account_number
        )

        with db.session() as session:
            session.add(account)
            session.flush()
            session.refresh(account)

        return account



trade_repository = TradeRepository()
signal_repository = SignalRepository()
account_repository = AccountRepository()