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
		'quantity': 'INTEGER DEFAULT 1 NOT NULL',
	}
	for name, sql_type in required.items():
		if name not in columns:
			conn.execute(text(f'ALTER TABLE transactions ADD COLUMN {name} {sql_type}'))


def seed(db: Session):
	# Seed user and sample transactions only if no users exist
	user_count = db.scalar(select(func.count()).select_from(User))
	if user_count == 0:
		seed_user = crud_user.create(
			db,
			obj_in=UserCreate(email="seed@example.com", full_name="Seed User", is_active=True)
		)
		today = date.today()
		for title, transaction_type, amount_per_unit in [
			("Coffee", TransactionType.expense, Decimal('5.00')),
			("Salary", TransactionType.earning, Decimal('1000.00')),
			("Owner Capital", TransactionType.capital, Decimal('5000.00')),
		]:
			crud_transaction.create(
				db,
				obj_in=TransactionCreate(
					title=title,
					description=None,
					owner_id=seed_user.id,
					transaction_type=transaction_type,
					amount_per_unit=amount_per_unit,
					quantity=1,
					date=today,
				),
			)

	# Seed Categories (always ensure presence)
	category_names = ["LPG", "Butane", "Coca-cola", "Pepsi Softdrinks", "Beer"]
	existing_categories = {c.name for c in db.scalars(select(Category)).all()}
	for name in category_names:
		if name not in existing_categories:
			crud_category.create(db, CategoryCreate(name=name, description=None))

	# Seed Weights (always ensure presence)
	weight_names = ["11kg", "225g", "170g", "500ml", "355ml (12oz)", "235ml (8oz)", "1L"]
	existing_weights = {w.name for w in db.scalars(select(Weight)).all()}
	for name in weight_names:
		if name not in existing_weights:
			crud_weight.create(db, WeightCreate(name=name, description=None))

	# Seed Inventory (sample items with category and weight references)
	inventory_count = db.scalar(select(func.count()).select_from(Inventory))
	if inventory_count == 0:
		# Get category and weight references
		lpg_cat = db.scalars(select(Category).where(Category.name == "LPG")).first()
		butane_cat = db.scalars(select(Category).where(Category.name == "Butane")).first()
		cocacola_cat = db.scalars(select(Category).where(Category.name == "Coca-cola")).first()
		pepsi_cat = db.scalars(select(Category).where(Category.name == "Pepsi Softdrinks")).first()
		beer_cat = db.scalars(select(Category).where(Category.name == "Beer")).first()
		
		weight_11kg = db.scalars(select(Weight).where(Weight.name == "11kg")).first()
		weight_225g = db.scalars(select(Weight).where(Weight.name == "225g")).first()
		weight_500ml = db.scalars(select(Weight).where(Weight.name == "500ml")).first()
		weight_355ml = db.scalars(select(Weight).where(Weight.name == "355ml (12oz)")).first()
		
		# Create sample inventory items
		sample_inventory = [
			("LPG Gas Tank", "LPG-11", Decimal('650.00'), Decimal('850.00'), 10, lpg_cat.id, weight_11kg.id),
			("Butane Canister", "BUT-225", Decimal('45.00'), Decimal('65.00'), 25, butane_cat.id, weight_225g.id),
			("Coca-Cola Bottle", "COKE-500", Decimal('18.00'), Decimal('25.00'), 50, cocacola_cat.id, weight_500ml.id),
			("Pepsi Can", "PEPSI-355", Decimal('15.00'), Decimal('22.00'), 40, pepsi_cat.id, weight_355ml.id),
			("Beer Bottle", "BEER-355", Decimal('30.00'), Decimal('45.00'), 30, beer_cat.id, weight_355ml.id),
		]
		
		for name, shortname, purchase, selling, qty, cat_id, wt_id in sample_inventory:
			crud_inventory.create(
				db,
				obj_in=InventoryCreate(
					name=name,
					shortname=shortname,
					purchase_price=purchase,
					selling_price=selling,
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
