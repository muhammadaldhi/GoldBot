from datetime import datetime
from typing import Dict, Any, Optional


class MT5Bridge:

    def __init__(self):

        self.connected: bool = False

        self.symbol: Optional[str] = None

        self.last_tick: Dict[str, Any] = {}

        self.last_seen: Optional[datetime] = None


    def connect(
        self,
        data: Dict[str, Any]
    ):

        self.connected = True

        self.symbol = data.get(
            "symbol"
        )

        self.last_seen = datetime.utcnow()


    def update_tick(
        self,
        data: Dict[str, Any]
    ):

        self.last_tick = data

        self.last_seen = datetime.utcnow()

        if not self.connected:
            self.connected = True

            self.symbol = data.get(
            "symbol"
        )


    def status(self):

        return {

            "connected": self.connected,

            "symbol": self.symbol,

            "last_tick": self.last_tick,

            "last_seen": self.last_seen

        }


    def is_alive(
        self,
        timeout: int = 15
    ) -> bool:

        if not self.last_seen:
            return False


        diff = (
            datetime.utcnow()
            -
            self.last_seen
        ).seconds


        return diff <= timeout



bridge = MT5Bridge()