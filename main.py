# Entry point will be implemented after scaffolding.
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import inspect, text
from sqlalchemy.orm import Session
from datetime import date
from decimal import Decimal

from app.core.config import settings
from app.db.session import Base, engine, SessionLocal
from app.models.user import User
from app.models.transaction import Transaction, TransactionType
from app.models.category import Category
from app.models.weight import Weight
from app.models.inventory import Inventory
from app.crud import user as crud_user
from app.crud import item as crud_transaction
from app.crud import category as crud_category
from app.crud import weight as crud_weight
from app.crud import inventory as crud_inventory
from app.schemas.user import UserCreate
from app.schemas.item import TransactionCreate
from app.schemas.category import CategoryCreate
from app.schemas.weight import WeightCreate
from app.schemas.inventory import InventoryCreate
from sqlalchemy import select, func
from app.routers.user import router as users_router
from app.routers.item import router as transactions_router
from app.routers.category import router as categories_router
from app.routers.weight import router as weights_router
from app.routers.inventory import router as inventory_router


app = FastAPI(title=settings.app_name, debug=settings.debug)

app.add_middleware(
	CORSMiddleware,
	allow_origins=settings.cors_allow_origins,
	allow_credentials=True,
	allow_methods=["*"],
	allow_headers=["*"],
)

app.include_router(users_router)
app.include_router(transactions_router)
app.include_router(categories_router)
app.include_router(weights_router)
app.include_router(inventory_router)


def enforce_columns(conn):
	inspector = inspect(conn)
	columns = {c['name']: c for c in inspector.get_columns('transactions')} if inspector.has_table('transactions') else {}
	required = {
		'transaction_type': 'TEXT',
		'amount': 'INTEGER',
		'date': 'DATE',
		'inventory_id': 'INTEGER',
		'quantity': 'NUMERIC(10, 3) DEFAULT 1.000 NOT NULL',
	}
	for name, sql_type in required.items():
		if name not in columns:
			conn.execute(text(f'ALTER TABLE transactions ADD COLUMN {name} {sql_type}'))


def seed(db: Session):
	# Seed user only if no users exist
	user_count = db.scalar(select(func.count()).select_from(User))
	if user_count == 0:
		crud_user.create(
			db,
			obj_in=UserCreate(
				email="dawnblaze.wholesale.distributions@gmail.com",
				full_name="DB Wholesale Trading",
				is_active=True
			)
		)

	# Seed Categories (always ensure presence)
	category_names = [
		"LPG",
		"Butane",
		"Coca-cola Soft Drinks",
		"Pepsi Soft Drinks",
		"Beer"
	]
	existing_categories = {c.name for c in db.scalars(select(Category)).all()}
	for name in category_names:
		if name not in existing_categories:
			crud_category.create(db, CategoryCreate(name=name, description=None))

	# Seed Weights (always ensure presence)
	weight_names = [
		"11kg",
		"225g",
		"170g",
		"500mL",
		"355ml (12oz)",
		"235ml (8oz)",
		"1L",
		"190mL",
		"290mL",
		"1.5L"
	]
	existing_weights = {w.name for w in db.scalars(select(Weight)).all()}
	for name in weight_names:
		if name not in existing_weights:
			crud_weight.create(db, WeightCreate(name=name, description=None))

	# Seed Inventory (actual inventory items)
	inventory_count = db.scalar(select(func.count()).select_from(Inventory))
	if inventory_count == 0:
		# Get category references
		lpg_cat = db.scalars(select(Category).where(Category.name == "LPG")).first()
		butane_cat = db.scalars(select(Category).where(Category.name == "Butane")).first()
		cocacola_cat = db.scalars(select(Category).where(Category.name == "Coca-cola Soft Drinks")).first()
		pepsi_cat = db.scalars(select(Category).where(Category.name == "Pepsi Soft Drinks")).first()
		beer_cat = db.scalars(select(Category).where(Category.name == "Beer")).first()
		
		# Get weight references
		weight_11kg = db.scalars(select(Weight).where(Weight.name == "11kg")).first()
		weight_225g = db.scalars(select(Weight).where(Weight.name == "225g")).first()
		weight_170g = db.scalars(select(Weight).where(Weight.name == "170g")).first()
		weight_500ml = db.scalars(select(Weight).where(Weight.name == "500mL")).first()
		weight_355ml = db.scalars(select(Weight).where(Weight.name == "355ml (12oz)")).first()
		weight_235ml = db.scalars(select(Weight).where(Weight.name == "235ml (8oz)")).first()
		weight_1L = db.scalars(select(Weight).where(Weight.name == "1L")).first()
		weight_190ml = db.scalars(select(Weight).where(Weight.name == "190mL")).first()
		weight_290ml = db.scalars(select(Weight).where(Weight.name == "290mL")).first()
		weight_1_5L = db.scalars(select(Weight).where(Weight.name == "1.5L")).first()
		
		# Create actual inventory items (name, shortname, quantity, category_id, weight_id)
		inventory_items = [
			("LPG", "LPG-11", Decimal('0.000'), lpg_cat.id, weight_11kg.id),
			("Butane 225g", "BUT-225", Decimal('0.000'), butane_cat.id, weight_225g.id),
			("Coca-Cola 1L", "COKE-500", Decimal('0.000'), cocacola_cat.id, weight_1L.id),
			("Pepsi 1L", "PEPSI-355", Decimal('0.000'), pepsi_cat.id, weight_1L.id),
			("Beer", "BEER-355", Decimal('0.000'), beer_cat.id, weight_355ml.id),
			("Butane 170g", None, Decimal('0.000'), butane_cat.id, weight_170g.id),
			("Coca-Cola 8oz", None, Decimal('0.000'), cocacola_cat.id, weight_235ml.id),
			("Pepsi 8oz", None, Decimal('0.000'), pepsi_cat.id, weight_235ml.id),
			("Pepsi 12oz", None, Decimal('0.000'), pepsi_cat.id, weight_355ml.id),
			("Coca-Cola 190mL", None, Decimal('0.000'), cocacola_cat.id, weight_190ml.id),
			("Coca-Cola 290mL", None, Decimal('0.000'), cocacola_cat.id, weight_290ml.id),
			("Coca-Cola 1.5L", None, Decimal('0.000'), cocacola_cat.id, weight_1_5L.id),
		]
		
		for name, shortname, qty, cat_id, wt_id in inventory_items:
			crud_inventory.create(
				db,
				obj_in=InventoryCreate(
					name=name,
					shortname=shortname,
					quantity=qty,
					category_id=cat_id,
					weight_id=wt_id,
				),
			)


@app.on_event("startup")
def on_startup():
	# Create tables
	Base.metadata.create_all(bind=engine)
	# Enforce columns for backward compatibility
	with engine.connect() as conn:
		enforce_columns(conn)
	# Note: Seeding is now manual via POST /seed endpoint


@app.get("/health")
def health():
	return {"status": "ok"}


@app.post("/seed")
def run_seed():
	"""Manually seed the database with initial data (users, transactions, categories, weights)."""
	db = SessionLocal()
	try:
		seed(db)
		return {"status": "ok", "message": "Database seeded successfully"}
	except Exception as e:
		return {"status": "error", "message": str(e)}
	finally:
		db.close()
