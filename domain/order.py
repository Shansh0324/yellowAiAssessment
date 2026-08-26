from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime
from domain.enums import OrderStatus

class OrderItem(BaseModel):
    sku: str
    name: str
    category: str
    size: str
    qty: int
    price: float
    final_sale: bool
    shipped: Optional[bool] = None
    backorder_eta: Optional[str] = None
    
    # We map item_id to sku for our return logic
    @property
    def item_id(self):
        return self.sku
        
    @property
    def is_final_sale(self):
        return self.final_sale
        
    @property
    def is_returnable(self):
        return self.category != "jewellery"

class Order(BaseModel):
    order_id: str
    customer_id: str
    status: str
    placed_at: datetime
    delivered_at: Optional[datetime] = None
    expected_delivery: Optional[str] = None
    carrier: Optional[str] = None
    tracking_number: Optional[str] = None
    payment_method: Optional[str] = None
    shipping_city: Optional[str] = None
    items: List[OrderItem]
    total: float
    cancelled_at: Optional[str] = None
    refund_status: Optional[str] = None
