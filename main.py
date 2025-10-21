# Entry point will be implemented after scaffolding.
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import inspect, text
from sqlalchemy.orm import Session
from datetime import date

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
	}
	for name, sql_type in required.items():
		if name not in columns:
			conn.execute(text(f'ALTER TABLE transactions ADD COLUMN {name} {sql_type}'))


def seed(db: Session):
	# Seed only if no users
	user_count = db.scalar(select(func.count()).select_from(User))
	if user_count == 0:
		seed_user = crud_user.create(
			db,
			obj_in=UserCreate(email="seed@example.com", full_name="Seed User", is_active=True)
		)
		today = date.today()
		for title, transaction_type, amount in [
			("Coffee", TransactionType.expense, 5),
			("Salary", TransactionType.earning, 1000),
			("Owner Capital", TransactionType.capital, 5000),
		]:
			crud_transaction.create(
				db,
				obj_in=TransactionCreate(
					title=title,
					description=None,
					owner_id=seed_user.id,
					transaction_type=transaction_type,
					amount=amount,
					date=today,
				),
			)

		# Seed Categories
		category_names = ["LPG", "Butane", "Coca-cola", "Pepsi Softdrinks", "Beer"]
		existing_categories = {c.name for c in db.scalars(select(Category)).all()}
		for name in category_names:
			if name not in existing_categories:
				crud_category.create(db, CategoryCreate(name=name, description=None))

		# Seed Weights
		weight_names = ["11kg", "225g", "170g", "500ml", "355ml (12oz)", "235ml (8oz)", "1L"]
		existing_weights = {w.name for w in db.scalars(select(Weight)).all()}
		for name in weight_names:
			if name not in existing_weights:
				crud_weight.create(db, WeightCreate(name=name, description=None))


@app.on_event("startup")
def on_startup():
	# Create tables
	Base.metadata.create_all(bind=engine)
	# Enforce columns for backward compatibility
	with engine.connect() as conn:
		enforce_columns(conn)
	# Seed
	db = SessionLocal()
	try:
		seed(db)
	finally:
		db.close()


@app.get("/health")
def health():
	return {"status": "ok"}
