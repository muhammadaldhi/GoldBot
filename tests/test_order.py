from backend.services.order_service import order_service


result = order_service.buy(
    "XAUUSD",
    0.01
)


print(result)