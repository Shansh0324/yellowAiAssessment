from pydantic import BaseModel

class Customer(BaseModel):
    customer_id: str
    email: str
    first_name: str
    last_name: str
