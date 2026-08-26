from services.orders.service import OrderService
from services.exchanges.service import ExchangeService
from domain.errors import DomainError
import json

order_service = OrderService()
exchange_service = ExchangeService()

def check_exchange_eligibility(order_id: str, customer_id: str, item_id: str) -> str:
    """Check if a specific item in an order is eligible for size exchange."""
    try:
        order = order_service.get_order(order_id, customer_id)
        is_eligible = exchange_service.check_eligibility(order, item_id)
        return json.dumps({"item_id": item_id, "is_eligible": is_eligible})
    except DomainError as e:
        return json.dumps({"error": str(e)})

def create_exchange(order_id: str, customer_id: str, items_to_exchange: list[dict]) -> str:
    """Create an exchange request for specified items."""
    try:
        order = order_service.get_order(order_id, customer_id)
        exchange_req = exchange_service.create_exchange(order, items_to_exchange)
        return exchange_req.model_dump_json()
    except DomainError as e:
        return json.dumps({"error": str(e)})
