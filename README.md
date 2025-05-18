# Cinch Product Rental API

Overview

This is a FastAPI application for a Product Rental Service, supporting product details, attributes, rental periods, and regional pricing.

## Setup

Clone the repository:
```bash
git clone git@github.com:Senzdamsik/cinch_fakhri.git
cd cinch_fakhri
```

Install dependencies:
```bash
uv sync
```

Set up environment variables: Create a .env file:
```bash
DATABASE_URL=postgresql+psycopg2://postgres:postgres@localhost:5433/test-cinch
```

## Running the Application

### Using Docker Compose (Recommended)
```bash
docker-compose up --build
```

### Local Development
1. Start PostgreSQL:
```bash
docker-compose up -d db
```

2. Run migrations:
```bash
uv run alembic upgrade head
```

3. Start the API:
```bash
uv run uvicorn app.main:app --host 0.0.0.0 --port 8000
```

## Running Tests

Tests can be run directly using pytest:

```bash
# Run all tests
pytest

# Run specific test file
pytest path/to/test_file.py

# Run specific test function
pytest path/to/test_file.py::test_function_name
```

The test configuration will automatically:
- Detect the environment (Docker/local/remote)
- Set up the test database
- Run migrations
- Clean up after tests

You can customize the test database connection using environment variables:
- `TEST_DATABASE_URL`: Complete database URL (overrides other settings if set)
- `POSTGRES_USER`: Database username (default: postgres)
- `POSTGRES_PASSWORD`: Database password (default: postgres)
- `POSTGRES_HOST`: Database host (default: localhost)
- `POSTGRES_PORT`: Database port (default: 5433)
- `TEST_DB_NAME`: Test database name (default: test-cinch-test)

## Database Seeding

To populate the database with example data:

1. Ensure PostgreSQL is running:
```bash
docker-compose up -d db
```

2. Run the SQL script:
```bash
psql -U postgres -h localhost -p 5433 -d test-cinch -f scripts/populate_tables.sql
```

## API Endpoints

### GET /products/{product_id}
Retrieve product details with attributes, rental periods, and regional pricing.

Query params: attributes_page, attributes_per_page for pagination.

Sample JSON Response:
```json
{
  "id": 1,
  "name": "Laptop",
  "description": "Gaming Laptop",
  "sku": "LAP123",
  "attributes": [
    {
      "id": 1,
      "name": "Color",
      "values": [
        {"id": 1, "value": "Black"}
      ]
    }
  ],
  "pricings": [
    {
      "rental_period": 3,
      "region": "Singapore",
      "price": 100.0
    }
  ]
}