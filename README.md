# Cinch Product Rental API

This is a FastAPI application for Fakhri's Senior Python Developer test at Cinch. The app allows users to retrieve complete product information including attributes, rental periods, and region-specific pricing.

You can access the live app at: https://cinch-fakhri-service-171906912767.asia-southeast1.run.app/docs/

## Prerequisites

Before you begin, ensure you have installed:
- Python 3.10 or higher
- Docker and Docker Compose (if using Docker)
- PostgreSQL (if running locally)
- `uv` package manager

### Installing UV

```bash
# Install uv using curl
curl -LsSf https://astral.sh/uv/install.sh | sh

# Or using pip
pip install uv
```

## Setup and Running

### Local Environment

1. Create and activate virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate
```

2. Install dependencies:
```bash
uv sync
```

3. Set up environment variables:
```bash
cp .env.example .env
# Edit .env file with your database credentials
```

4. Run the application:
```bash
# Run migrations
alembic upgrade head

# Start the API server
uvicorn app.main:app --reload

# Populate sample data
psql -U your_username -h localhost -p 5432 -d test-cinch -f scripts/populate_tables.sql

# Run tests
pytest -v
```

### Docker Environment

1. Build and start containers:
```bash
docker compose up --build -d
```

2. Run tests in container:
```bash
docker compose exec app pytest app/tests -v
```

## API Response Example

GET `/products/1`

```json
{
  "id": 1,
  "name": "Laptop",
  "description": "High-performance gaming laptop",
  "sku": "LAP123",
  "attributes": [
    {
      "id": 1,
      "name": "Color",
      "values": [
        {
          "id": 1,
          "value": "Black"
        },
        {
          "id": 2,
          "value": "Silver"
        }
      ]
    },
    {
      "id": 2,
      "name": "Storage",
      "values": [
        {
          "id": 3,
          "value": "256GB"
        },
        {
          "id": 4,
          "value": "512GB"
        }
      ]
    }
  ],
  "pricings": [
    {
      "rental_period": 12,
      "region": "Singapore",
      "price": 350
    },
    {
      "rental_period": 6,
      "region": "Singapore",
      "price": 180
    },
    {
      "rental_period": 3,
      "region": "Singapore",
      "price": 100
    },
    {
      "rental_period": 12,
      "region": "Malaysia",
      "price": 340
    },
    {
      "rental_period": 6,
      "region": "Malaysia",
      "price": 170
    },
    {
      "rental_period": 3,
      "region": "Malaysia",
      "price": 90
    }
  ]
}
```

