from services.orders.service import OrderService
from services.returns.service import ReturnService
from domain.errors import DomainError
import json

order_service = OrderService()
return_service = ReturnService()

def check_return_eligibility(order_id: str, customer_id: str, item_id: str) -> str:
    """Check if a specific item in an order is eligible for return."""
    try:
        order = order_service.get_order(order_id, customer_id)
        is_eligible = return_service.check_eligibility(order, item_id)
        return json.dumps({"item_id": item_id, "is_eligible": is_eligible})
    except DomainError as e:
        return json.dumps({"error": str(e)})

def create_return(order_id: str, customer_id: str, items_to_return: list[dict]) -> str:
    """Create a return request for specified items."""
    try:
        order = order_service.get_order(order_id, customer_id)
        return_req = return_service.create_return(order, items_to_return)
        return return_req.model_dump_json()
    except DomainError as e:
        return json.dumps({"error": str(e)})
