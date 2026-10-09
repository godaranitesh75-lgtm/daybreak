from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database import SessionLocal
from app.models import models
from app.schemas import schemas

router = APIRouter(prefix="/orders", tags=["orders"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/", response_model=List[schemas.Order])
def get_orders(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    orders = db.query(models.Order).order_by(models.Order.id.desc()).offset(skip).limit(limit).all()
    return orders

@router.get("/{order_id}", response_model=schemas.Order)
def get_order(order_id: int, db: Session = Depends(get_db)):
    order = db.query(models.Order).filter(models.Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order

@router.post("/", response_model=schemas.Order)
def create_order(order: schemas.OrderCreate, db: Session = Depends(get_db)):
    if not order.items:
        raise HTTPException(status_code=400, detail="An order must contain at least one item")

    products = {}
    quantities = {}
    for item in order.items:
        if item.quantity < 1:
            raise HTTPException(status_code=400, detail="Item quantities must be at least 1")
        quantities[item.product_id] = quantities.get(item.product_id, 0) + item.quantity

    total = 0.0
    for product_id, quantity in quantities.items():
        product = db.query(models.Product).filter(models.Product.id == product_id).first()
        if not product:
            raise HTTPException(status_code=404, detail=f"Product {product_id} not found")
        if product.stock < quantity:
            raise HTTPException(status_code=400, detail=f"Not enough stock for {product.name}")
        products[product_id] = product
        total += product.price * quantity

    total = round(total * 1.08, 2)

    db_order = models.Order(
        customer_name=order.customer_name.strip() or "Walk-in customer",
        total_amount=total,
        status=models.OrderStatus.PENDING,
    )
    db.add(db_order)
    db.flush()

    for product_id, quantity in quantities.items():
        product = products[product_id]
        db.add(models.OrderItem(
            order_id=db_order.id,
            product_id=product_id,
            quantity=quantity,
            price=product.price,
        ))
        product.stock -= quantity

    db.commit()
    db.refresh(db_order)
    return db_order

@router.put("/{order_id}/status")
def update_order_status(order_id: int, status: models.OrderStatus, db: Session = Depends(get_db)):
    db_order = db.query(models.Order).filter(models.Order.id == order_id).first()
    if not db_order:
        raise HTTPException(status_code=404, detail="Order not found")
    db_order.status = status
    db.commit()
    db.refresh(db_order)
    return db_order
