from typing import Dict, Any

from backend.utils import get_logger, trade_logger
from backend.mt5_bridge import bridge
from backend.database.repository import order_repository


logger = get_logger()

trade_log = trade_logger()



class OrderService:


    def send_order(
        self,
        order: Dict[str, Any]
    ):

        if not bridge.connected:

            return {
                "status": "failed",
                "reason": "MT5 disconnected"
            }


        saved = order_repository.create(

            symbol=order["symbol"],

            action=order["action"],

            volume=order.get(
                "volume",
                0.01
            ),

            sl=order.get(
                "sl",
                0
            ),

            tp=order.get(
                "tp",
                0
            ),

            magic=order.get(
                "magic",
                777001
            ),

            comment=order.get(
                "comment",
                "GoldBot"
            )

        )


        trade_log.info(
            f"QUEUE "
            f"{saved.action} "
            f"{saved.symbol} "
            f"{saved.volume}"
        )


        logger.info(
            f"Order queued ID={saved.id}"
        )


        return {

            "status": "queued",

            "order_id": saved.id

        }



order_service = OrderService()