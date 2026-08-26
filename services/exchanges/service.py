from domain.order import Order
from domain.exchange_request import ExchangeRequest, ExchangeItem
from domain.enums import ExchangeStatus
from domain.errors import InvalidExchangeRequestError
from datetime import datetime, timezone
import uuid

class ExchangeService:
    def check_eligibility(self, order: Order, item_id: str) -> bool:
        item = next((i for i in order.items if i.item_id == item_id), None)
        if not item:
            return False
            
        if not order.delivered_at:
            return False
            
        days_since_delivery = (datetime.now(timezone.utc) - order.delivered_at).days
        if days_since_delivery > 30:
            return False
            
        return True

    def create_exchange(self, order: Order, items_to_exchange: list[dict]) -> ExchangeRequest:
        exchange_items = []
        
        for req_item in items_to_exchange:
            item_id = req_item['item_id']
            if not self.check_eligibility(order, item_id):
                raise InvalidExchangeRequestError(f"Item {item_id} is not eligible for exchange.")
            
            exchange_items.append(ExchangeItem(
                item_id=item_id,
                quantity=req_item['quantity'],
                new_size=req_item['new_size'],
                reason=req_item['reason']
            ))
            
        return ExchangeRequest(
            exchange_id=f"EXC-{uuid.uuid4().hex[:6].upper()}",
            order_id=order.order_id,
            customer_id=order.customer_id,
            status=ExchangeStatus.APPROVED,
            items=exchange_items,
            created_at=datetime.now(timezone.utc)
        )
