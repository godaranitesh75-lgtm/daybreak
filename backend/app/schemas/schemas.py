from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from app.models.models import ProductCategory, OrderStatus

class ProductBase(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    category: ProductCategory
    stock: int = 0

class ProductCreate(ProductBase):
    pass

class ProductUpdate(ProductBase):
    pass

class Product(ProductBase):
    id: int

    class Config:
        from_attributes = True

class OrderItemBase(BaseModel):
    product_id: int
    quantity: int

class OrderItemCreate(OrderItemBase):
    pass

class OrderItem(OrderItemBase):
    id: int
    price: float

    class Config:
        from_attributes = True

class OrderBase(BaseModel):
    customer_name: str

class OrderCreate(OrderBase):
    items: List[OrderItemCreate]

class OrderUpdateStatus(BaseModel):
    status: OrderStatus

class Order(OrderBase):
    id: int
    order_date: datetime
    status: OrderStatus
    total_amount: float
    items: List[OrderItem]

    class Config:
        from_attributes = True
