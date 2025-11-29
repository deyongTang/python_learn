# FastAPI + MySQL RBAC Sample

This example demonstrates how to wire FastAPI, Pydantic v2, and SQLAlchemy's async engine against a MySQL database using a minimal RBAC schema.

## Requirements

* Python 3.11+
* A running MySQL instance reachable from the app (the default URL expects `mysql+aiomysql://user:password@localhost:3306/fastapi_rbac`).

Install dependencies:

```bash
pip install -r requirements.txt
```

## Running the API

1. Export or place your connection string in `.env` using the key `DATABASE_URL` if you want to override the default.
2. Start the development server:

```bash
uvicorn fastapi_mysql_rbac.app.main:app --reload
```

The app will automatically create the RBAC tables at startup.

## Example workflow

```bash
# Create permissions
curl -X POST http://127.0.0.1:8000/permissions -H "Content-Type: application/json" \
  -d '{"name":"view_reports","description":"View reporting dashboard"}'

# Create a role and attach the permission
curl -X POST http://127.0.0.1:8000/roles -H "Content-Type: application/json" \
  -d '{"name":"analyst","description":"Can view reports"}'
curl -X POST http://127.0.0.1:8000/roles/1/permissions/1

# Create a user and assign the role
curl -X POST http://127.0.0.1:8000/users -H "Content-Type: application/json" \
  -d '{"email":"ada@example.com","full_name":"Ada Lovelace"}'
curl -X POST http://127.0.0.1:8000/users/1/roles/1

# Fetch effective permissions for the user
curl http://127.0.0.1:8000/users/1/permissions
```
