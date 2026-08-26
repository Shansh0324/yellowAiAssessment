from domain.order import Order
from domain.return_request import ReturnRequest, ReturnItem
from domain.enums import ReturnStatus
from domain.errors import InvalidReturnRequestError
from datetime import datetime, timezone
import uuid

class ReturnService:
    def check_eligibility(self, order: Order, item_id: str) -> bool:
        # Business rule logic
        item = next((i for i in order.items if i.item_id == item_id), None)
        if not item:
            return False
            
        if not item.is_returnable or item.is_final_sale:
            return False
            
        if not order.delivered_at:
            return False
            
        days_since_delivery = (datetime.now(timezone.utc) - order.delivered_at).days
        if days_since_delivery > 30:
            return False
            
        return True

    def create_return(self, order: Order, items_to_return: list[dict]) -> ReturnRequest:
        return_items = []
        total_refund = 0.0
        
        for req_item in items_to_return:
            item_id = req_item['item_id']
            if not self.check_eligibility(order, item_id):
                raise InvalidReturnRequestError(f"Item {item_id} is not eligible for return.")
            
            # Find price
            order_item = next(i for i in order.items if i.item_id == item_id)
            total_refund += order_item.price * req_item['quantity']
            
            return_items.append(ReturnItem(
                item_id=item_id,
                quantity=req_item['quantity'],
                reason=req_item['reason']
            ))
            
        return ReturnRequest(
            return_id=f"RET-{uuid.uuid4().hex[:6].upper()}",
            order_id=order.order_id,
            customer_id=order.customer_id,
            status=ReturnStatus.APPROVED,
            items=return_items,
            created_at=datetime.now(timezone.utc),
            refund_amount=total_refund
        )
