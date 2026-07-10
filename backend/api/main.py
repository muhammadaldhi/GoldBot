from fastapi import Request
from fastapi import FastAPI

from backend.utils import get_logger
from backend.mt5_bridge import bridge
from backend.services.order_service import order_service
from backend.services.order_queue import order_queue


logger = get_logger()


app = FastAPI(
    title="GoldBot API",
    version="1.0.0"
)


@app.get("/")
def home():

    logger.info(
        "GoldBot API running"
    )

    return {
        "app": "GoldBot",
        "status": "running"
    }




@app.post("/mt5/connect")
async def mt5_connect(
    request: Request
):

    data = await request.json()


    bridge.connect(
        data
    )


    logger.info(
        f"MT5 connected: {data}"
    )


    return {
        "status": "connected"
    }



@app.post("/mt5/tick")
async def mt5_tick(
    request: Request
):

    data = await request.json()


    bridge.update_tick(
        data
    )


    logger.info(
        f"Tick received: {data}"
    )


    return {
        "status": "received"
    }



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

@app.post("/order")
async def create_order(
    request: Request
):

    data = await request.json()

    result = order_service.send_order(
        data
    )

    return result

@app.get("/mt5/order")
def get_mt5_order():

    order = order_queue.get_next()


    if not order:

        return {
            "status": "empty"
        }


    return order

@app.post("/mt5/order/{order_id}/failed")
def failed_order(
    order_id:int,
    request:Request
):

    result = order_queue.failed(
        order_id,
        "MT5 execution failed"
    )


    return {
        "status":"failed",
        "order":result
    }