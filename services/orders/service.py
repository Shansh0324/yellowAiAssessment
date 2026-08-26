import json
from typing import List, Optional
from domain.order import Order
from domain.errors import OrderNotFoundError, UnauthorizedAccessError

class OrderService:
    def __init__(self, data_path: str = "data/orders.json"):
        self.data_path = data_path
        self.orders = self._load_orders()

    def _load_orders(self) -> List[Order]:
        try:
            with open(self.data_path, "r") as f:
                data = json.load(f)
                # handle if data is just list or dict containing 'orders' key
                orders_data = data.get("orders", []) if isinstance(data, dict) else data
                return [Order(**order) for order in orders_data]
        except FileNotFoundError:
            return []

    def get_order(self, order_id: str, customer_id: str) -> Order:
        for order in self.orders:
            if order.order_id == order_id:
                if order.customer_id != customer_id:
                    raise UnauthorizedAccessError(f"Customer {customer_id} not authorized to access order {order_id}")
                return order
        raise OrderNotFoundError(f"Order {order_id} not found.")

    def get_orders_by_customer(self, customer_id: str) -> List[Order]:
        return [o for o in self.orders if o.customer_id == customer_id]
