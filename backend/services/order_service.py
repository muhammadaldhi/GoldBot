from typing import Dict, Any

from backend.utils import get_logger, trade_logger
from backend.mt5_bridge import bridge
from backend.services.order_queue import order_queue


logger = get_logger()
trade_log = trade_logger()



class OrderService:


    def buy(
        self,
        symbol: str,
        lot: float
    ):

        return self.send_order(
            {
                "action": "BUY",
                "symbol": symbol,
                "lot": lot
            }
        )



    def sell(
        self,
        symbol: str,
        lot: float
    ):

        return self.send_order(
            {
                "action": "SELL",
                "symbol": symbol,
                "lot": lot
            }
        )



    def send_order(
        self,
        order: Dict[str, Any]
    ):


        if not bridge.connected:

            logger.error(
                "MT5 disconnected"
            )

            return {
                "status":"failed",
                "reason":"MT5 disconnected"
            }



        required = [
            "action",
            "symbol",
            "lot"
        ]


        for field in required:

            if field not in order:

                return {
                    "status":"failed",
                    "reason":f"missing {field}"
                }



        if order["action"] not in [
            "BUY",
            "SELL"
        ]:

            return {
                "status":"failed",
                "reason":"invalid action"
            }



        queued = order_queue.add(
            order
        )


        trade_log.info(
            f"{order['action']} "
            f"{order['symbol']} "
            f"{order['lot']}"
        )


        logger.info(
            f"Order queued: {queued}"
        )


        return {
            "status":"queued",
            "order":queued
        }



order_service = OrderService()