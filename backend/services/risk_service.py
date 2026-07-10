from backend.database.repository import position_repository


class RiskManager:


    MAX_POSITION = 1



    def can_trade(
        self,
        symbol="XAUUSD"
    ):

        positions = (
            position_repository
            .get_open()
        )


        active = [
            p for p in positions
            if p.symbol == symbol
        ]


        if len(active) >= self.MAX_POSITION:

            return {

                "allowed": False,

                "reason":
                "maximum position reached"

            }



        return {

            "allowed": True,

            "reason":
            "risk check passed"

        }



risk_manager = RiskManager()