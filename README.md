# Daybreak Coffee Shop Manager

A small coffee shop point-of-sale and management app built with FastAPI, SQLAlchemy, SQLite/PostgreSQL, and a responsive HTML dashboard.

## Project structure

```text
frontend/           Coffee shop dashboard
backend/            FastAPI application and database models
	app/
	requirements.txt
pyproject.toml       Vercel FastAPI entrypoint
```

## Features

- Menu browsing with category filters and search
- Cart checkout with stock checks and order totals
- Order queue with status updates
- Inventory restocking and menu item management
- Dashboard sales and stock summaries
- Automatic starter menu and table creation on first startup

## Run locally

Start the backend in one terminal:

```powershell
cd backend
..\.venv\Scripts\python.exe -m pip install -r requirements.txt
..\.venv\Scripts\python.exe -m uvicorn app.main:app --reload
```

Start the frontend in another terminal:

```powershell
cd frontend
npm install
npm run dev
```

Open the Vite URL printed in the frontend terminal. Its dev proxy forwards API requests to `http://127.0.0.1:8000`. The backend also serves the page at `http://127.0.0.1:8000`; API documentation is at `http://127.0.0.1:8000/docs`.

## Deploy the frontend separately

For a Render Static Site, use root directory `frontend`, build command `npm run build`, and publish directory `dist`. Set the `VITE_API_BASE_URL` environment variable to the deployed backend URL, with no trailing slash.

## Use Neon PostgreSQL

Create `backend/.env` and add the Neon connection string without surrounding quotes:

```env
DATABASE_URL=postgresql://USER:PASSWORD@HOST/DATABASE?sslmode=require
```

The app loads this file on startup, uses the PostgreSQL driver, and creates the `products`, `orders`, and `order_items` tables automatically. Keep `.env` private; it is excluded from Git. If `DATABASE_URL` is not set, the app uses the local SQLite database.

## Main API routes

- `GET/POST /products/` - list and add menu items
- `PUT/DELETE /products/{product_id}` - update or remove menu items
- `GET/POST /orders/` - list or create orders
- `PUT /orders/{order_id}/status?status=preparing` - update an order status
- `GET /docs` - interactive API documentation
