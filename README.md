# FastAPI CRUD Application

Implements Users and Transactions with search and seeded data.

## Quick Start (Windows PowerShell)
```
python -m venv venv
venv\Scripts\Activate.ps1
pip install -r requirements.txt
python -m uvicorn main:app --reload
```

## Endpoints
- /users CRUD
- /transactions CRUD
- /transactions/search with filters: owner_id, q, transaction_type, date_from, date_to, skip, limit
- /categories CRUD
- /weights CRUD
- /inventory CRUD

## Health
GET /health -> {"status":"ok"}

## Maintenance Rule
Any code change affecting models, endpoints, enums, or seeding must update `.github/application-setup.yml` and `.cursor/rules/application-setup.mdc` in the same commit. See `CONTRIBUTING.md` for details.

## Relationships
Transactions optionally reference an Inventory item via `inventory_id` (nullable). Inventory lists its related Transactions.
