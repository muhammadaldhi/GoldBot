from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional


@dataclass
class BotState:
    """
    Menyimpan kondisi runtime GoldBot.
    """

    running: bool = False

    connected: bool = False

    last_signal: Optional[str] = None

    active_symbol: Optional[str] = None

    active_trade_id: Optional[int] = None

    started_at: Optional[datetime] = None

    total_trades: int = 0

    daily_profit: float = 0.0

    last_error: Optional[str] = None


    def start(self):
        self.running = True
        self.started_at = datetime.utcnow()


    def stop(self):
        self.running = False


    def reset_error(self):
        self.last_error = None


state = BotState()