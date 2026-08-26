from services.orders.service import OrderService
from domain.errors import DomainError
import json

order_service = OrderService()

def get_order(order_id: str, customer_id: str) -> str:
    """Retrieve details for a specific order."""
    try:
        order = order_service.get_order(order_id, customer_id)
        return order.model_dump_json()
    except DomainError as e:
        return json.dumps({"error": str(e)})

def get_customer_orders(customer_id: str) -> str:
    """Retrieve all orders for a specific customer."""
    try:
        orders = order_service.get_orders_by_customer(customer_id)
        if not orders:
            return json.dumps({"message": f"No orders found for customer {customer_id}"})
        return json.dumps([json.loads(o.model_dump_json()) for o in orders])
    except Exception as e:
        return json.dumps({"error": str(e)})
