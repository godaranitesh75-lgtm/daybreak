from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from app.database import engine, Base
from app.database import SessionLocal
from app.models import models
from app.routes import products, orders

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Coffee Shop API", version="1.0.0")
INDEX_FILE = Path(__file__).resolve().parents[2] / "index.html"

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(products.router)
app.include_router(orders.router)

@app.on_event("startup")
def seed_products():
    db = SessionLocal()
    try:
        if db.query(models.Product).count() == 0:
            db.add_all([
                models.Product(name="Flat White", description="Double espresso, silky steamed milk", price=160.00, category=models.ProductCategory.COFFEE, stock=24),
                models.Product(name="Oat Cappuccino", description="Espresso with oat milk and cocoa", price=190.00, category=models.ProductCategory.COFFEE, stock=18),
                models.Product(name="Cold Brew", description="Slow-steeped for 18 hours", price=180.00, category=models.ProductCategory.COFFEE, stock=16),
                models.Product(name="Vanilla Latte", description="Espresso, vanilla and steamed milk", price=175.00, category=models.ProductCategory.COFFEE, stock=20),
                models.Product(name="Matcha Cloud", description="Ceremonial matcha with oat milk", price=210.00, category=models.ProductCategory.TEA, stock=12),
                models.Product(name="Chai Latte", description="Black tea with warming spices", price=140.00, category=models.ProductCategory.TEA, stock=15),
                models.Product(name="Butter Croissant", description="Flaky, baked fresh this morning", price=95.00, category=models.ProductCategory.PASTRY, stock=14),
                models.Product(name="Banana Bread", description="Toasted walnut and brown butter", price=110.00, category=models.ProductCategory.PASTRY, stock=9),
                models.Product(name="Avocado Toast", description="Sourdough, lemon and chili flakes", price=220.00, category=models.ProductCategory.SNACK, stock=8),
            ])
            db.commit()
    finally:
        db.close()

@app.get("/")
def root():
    return FileResponse(INDEX_FILE)

@app.get("/health")
def health():
    return {"message": "Coffee Shop API is running"}
