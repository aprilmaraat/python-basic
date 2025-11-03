# FastAPI CRUD Application

Implements Users and Transactions with search and seeded data.

## Quick Start (Windows PowerShell)
```
python -m venv venv
venv\Scripts\Activate.ps1
pip install -r requirements.txt
python -m uvicorn main:app --reload
```

## Seeding the Database
The application no longer seeds data automatically on startup. To seed the database with initial data, make a POST request to the `/seed` endpoint:

```powershell
# Using curl
curl -X POST http://127.0.0.1:8000/seed

# Or using Invoke-WebRequest (PowerShell)
Invoke-WebRequest -Uri http://127.0.0.1:8000/seed -Method POST
```

You can also use the interactive API docs at http://127.0.0.1:8000/docs and execute the POST /seed endpoint.

### What gets seeded:
- **Users**: 1 seed user (seed@example.com)
- **Transactions**: 3 sample transactions (Coffee, Salary, Owner Capital)
- **Categories**: LPG, Butane, Coca-cola, Pepsi Softdrinks, Beer
- **Weights**: 11kg, 225g, 170g, 500ml, 355ml (12oz), 235ml (8oz), 1L
- **Inventory**: 5 sample inventory items with proper category and weight references:
  - LPG Gas Tank (LPG + 11kg)
  - Butane Canister (Butane + 225g)
  - Coca-Cola Bottle (Coca-cola + 500ml)
  - Pepsi Can (Pepsi Softdrinks + 355ml)
  - Beer Bottle (Beer + 355ml)

## Endpoints
- /users CRUD
- /transactions CRUD
- /transactions/search with filters: owner_id, q, transaction_type, date_from, date_to, skip, limit
- /categories CRUD
- /weights CRUD
- /inventory CRUD
- /inventory/search with filters: q, category_id, weight_id, min_quantity, max_quantity, skip, limit
- /inventory/{id}/detailed - Get inventory with detailed category and weight information
- POST /seed - Manually seed the database with initial data

## Health
GET /health -> {"status":"ok"}

## Maintenance Rule
Any code change affecting models, endpoints, enums, or seeding must update `.github/application-setup.yml` and `.cursor/rules/application-setup.mdc` in the same commit. See `CONTRIBUTING.md` for details.

## Relationships
Transactions optionally reference an Inventory item via `inventory_id` (nullable). Inventory lists its related Transactions.
