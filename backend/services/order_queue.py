from typing import Dict, Any, List
from datetime import datetime
from threading import Lock


class OrderQueue:

    def __init__(self):

        self.queue: List[Dict[str, Any]] = []

        self.counter = 0

        self.lock = Lock()



    def add(
        self,
        order: Dict[str, Any]
    ):

        with self.lock:

            self.counter += 1

            order["id"] = self.counter

            order["created_at"] = (
                datetime.utcnow()
                .isoformat()
            )

            order["status"] = "pending"


            self.queue.append(
                order
            )


            return order



    def get_next(self):

        with self.lock:

            for order in self.queue:

                if order["status"] == "pending":

                    order["status"] = "processing"

                    order["taken_at"] = (
                        datetime.utcnow()
                        .isoformat()
                    )

                    return order


        return None



    def complete(
        self,
        order_id: int
    ):

        with self.lock:

            for order in self.queue:

                if order["id"] == order_id:

                    order["status"] = "executed"

                    order["completed_at"] = (
                        datetime.utcnow()
                        .isoformat()
                    )

                    return order


        return None



    def failed(
        self,
        order_id: int,
        reason: str
    ):

        with self.lock:

            for order in self.queue:

                if order["id"] == order_id:

                    order["status"] = "failed"

                    order["reason"] = reason

                    return order


        return None



    def all(self):

        return self.queue



order_queue = OrderQueue()