from fastapi import (
    FastAPI,
    Request,
)

from backend.utils import get_logger

from backend.mt5_bridge import bridge

from backend.services.order_service import (
    order_service
)

from backend.database.repository import (
    order_repository,
    position_repository,
)

from backend.database import db
from backend.database import models


logger = get_logger()


app = FastAPI(
    title="GoldBot API",
    version="2.0"
)



# ==========================================================
# STARTUP
# ==========================================================

@app.on_event("startup")
def startup_event():

    logger.info(
        "Initializing database"
    )


    db.initialize()

    db.create_tables()


    logger.info(
        "Database ready"
    )



# ==========================================================
# HOME
# ==========================================================

@app.get("/")
def home():

    return {

        "app": "GoldBot",

        "status": "running"

    }



# ==========================================================
# MT5 CONNECT
# ==========================================================

@app.post("/mt5/connect")
async def mt5_connect(
    request: Request
):

    data = await request.json()


    bridge.connect(
        data
    )


    logger.info(
        f"MT5 connected {data}"
    )


    return {

        "status": "connected"

    }



# ==========================================================
# MT5 TICK
# ==========================================================

@app.post("/mt5/tick")
async def mt5_tick(
    request: Request
):

    data = await request.json()


    bridge.update_tick(
        data
    )


    return {

        "status": "received"

    }



# ==========================================================
# STATUS
# ==========================================================

@app.get("/status")
def status():

    return {

        "connected":
            bridge.connected,

        "alive":
            bridge.is_alive(),

        "bridge":
            bridge.status()

    }



# ==========================================================
# CREATE ORDER
# ==========================================================

@app.post("/order")
async def create_order(
    request: Request
):

    data = await request.json()


    result = order_service.send_order(
        data
    )


    return result



# ==========================================================
# EA GET ORDER QUEUE
# ==========================================================

@app.get("/mt5/order")
def get_mt5_order():


    order = order_repository.get_next()


    if not order:

        return {

            "status": "empty"

        }


    return {

        "id":
            order.id,

        "action":
            order.action,

        "symbol":
            order.symbol,

        "volume":
            float(order.volume),

        "sl":
            order.sl,

        "tp":
            order.tp,

        "magic":
            order.magic,

        "comment":
            order.comment

    }



# ==========================================================
# EA ORDER DONE
# ==========================================================

@app.post("/mt5/order/{order_id}/done")
async def complete_order(
    order_id: int,
    request: Request
):

    data = await request.json()


    result = order_repository.complete(

        order_id,

        data.get(
            "ticket"
        )

    )


    if not result:

        return {

            "status": "failed",

            "reason": "order not found"

        }


    return {

        "status": "done",

        "order_id": result.id

    }



# ==========================================================
# EA ORDER FAILED
# ==========================================================

@app.post("/mt5/order/{order_id}/failed")
async def failed_order(
    order_id: int,
    request: Request
):

    data = await request.json()


    result = order_repository.failed(

        order_id,

        data.get(
            "error",
            "MT5 execution failed"
        )

    )


    if not result:

        return {

            "status": "failed",

            "reason": "order not found"

        }


    return {

        "status": "failed",

        "order_id": result.id

    }



# ==========================================================
# MT5 POSITION SYNC
# ==========================================================

@app.post("/mt5/positions")
async def sync_positions(
    request: Request
):

    positions = await request.json()


    logger.info(
        f"Position JSON received: {positions}"
    )


    if not isinstance(positions, list):

        return {

            "status": "failed",

            "reason": "payload must be list"

        }


    if len(positions) == 0:

        return {

            "status": "synced",

            "count": 0,

            "message": "no open positions"

        }


    saved = 0


    for pos in positions:

        try:

            position_repository.upsert(

                ticket=pos.get(
                    "ticket",
                    0
                ),

                symbol=pos.get(
                    "symbol",
                    ""
                ),

                position_type=pos.get(
                    "type",
                    ""
                ),

                volume=float(
                    pos.get(
                        "volume",
                        0
                    )
                ),

                price_open=float(
                    pos.get(
                        "price_open",
                        0
                    )
                ),

                price_current=float(
                    pos.get(
                        "price_current",
                        0
                    )
                ),

                sl=float(
                    pos.get(
                        "sl",
                        0
                    )
                ),

                tp=float(
                    pos.get(
                        "tp",
                        0
                    )
                ),

                profit=float(
                    pos.get(
                        "profit",
                        0
                    )
                ),

                swap=float(
                    pos.get(
                        "swap",
                        0
                    )
                ),

                commission=float(
                    pos.get(
                        "commission",
                        0
                    )
                ),

                magic=int(
                    pos.get(
                        "magic",
                        0
                    )
                ),

                comment=pos.get(
                    "comment",
                    ""
                )

            )

            saved += 1


        except Exception as e:

            logger.error(
                f"Position sync error: {e} | DATA={pos}"
            )


    return {

        "status": "synced",

        "count": saved

    }


# ==========================================================
# VIEW POSITIONS
# ==========================================================

@app.get("/positions")
def get_positions():

    positions = position_repository.get_all()


    return [

        {

            "ticket": p.ticket,

            "symbol": p.symbol,

            "type": p.type,

            "volume": p.volume,

            "profit": p.profit,

            "status": p.status

        }

        for p in positions

    ]



@app.get("/positions/open")
def get_open_positions():

    positions = position_repository.get_open()


    return [

        {

            "ticket": p.ticket,

            "symbol": p.symbol,

            "type": p.type,

            "volume": p.volume,

            "profit": p.profit

        }

        for p in positions

    ]


@app.get("/strategy/test")
def test_strategy():

    from backend.strategies.gold_strategy import GoldStrategy


    prices = [
        4100,
        4102,
        4105,
        4108,
        4110,
        4115,
        4118,
        4120
    ]


    engine = GoldStrategy()


    return engine.analyze(
        prices
    )