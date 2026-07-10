from backend.mt5_bridge import bridge
from backend.strategies.gold_strategy import GoldStrategy
from backend.database.repository import order_repository
from backend.services.risk_service import risk_manager


class StrategyService:


    def __init__(self):

        self.strategy = GoldStrategy()

        self.last_signal = None



    def run(self):

        prices = bridge.get_prices()


        result = self.strategy.analyze(
            prices
        )


        signal = result.get(
            "signal"
        )


        if signal == "HOLD":

            return result



        # cegah order berulang
        if signal == self.last_signal:

            return result



        self.last_signal = signal



        risk = risk_manager.can_trade(
            symbol="XAUUSD"
        )


        if not risk["allowed"]:

            result["risk"] = risk

            return result



        order = order_repository.create(

            symbol="XAUUSD",

            action=signal,

            volume=0.01,

            sl=0,

            tp=0,

            magic=777001,

            comment="GoldBot Strategy"

        )


        result["order_id"] = order.id


        result["risk"] = risk


        return result



strategy_service = StrategyService()