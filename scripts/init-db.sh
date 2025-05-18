#!/bin/bash

set -e

# Wait for PostgreSQL to be ready
until pg_isready; do
    echo "Waiting for PostgreSQL to be ready..."
    sleep 2
done

echo "PostgreSQL is ready"

# Create test-cinch database if it doesn't exist
psql -U postgres -tc "SELECT 1 FROM pg_database WHERE datname = 'test-cinch'" | grep -q 1 || psql -U postgres -c "CREATE DATABASE \"test-cinch\""

# Create test-cinch-dev database if it doesn't exist
psql -U postgres -tc "SELECT 1 FROM pg_database WHERE datname = 'test-cinch-dev'" | grep -q 1 || psql -U postgres -c "CREATE DATABASE \"test-cinch-dev\""

# Grant privileges
psql -U postgres -c "GRANT ALL PRIVILEGES ON DATABASE \"test-cinch\" TO postgres"
psql -U postgres -c "GRANT ALL PRIVILEGES ON DATABASE \"test-cinch-dev\" TO postgres"

# Run migrations using Alembic for test-cinch database
cd /app
export DATABASE_URL="postgresql://postgres:${POSTGRES_PASSWORD}@/test-cinch"
echo "Running migrations for test-cinch database..."
alembic upgrade head || { echo "Failed to run migrations for test-cinch"; exit 1; }

# Run migrations using Alembic for test-cinch-dev database
export DATABASE_URL="postgresql://postgres:${POSTGRES_PASSWORD}@/test-cinch-dev"
echo "Running migrations for test-cinch-dev database..."
alembic upgrade head || { echo "Failed to run migrations for test-cinch-dev"; exit 1; }

# Populate data for test-cinch database
echo "Populating initial data..."
psql -U postgres -d test-cinch -f /app/scripts/populate_tables.sql || { echo "Failed to populate test-cinch data"; exit 1; }

# Populate test data for test-cinch-dev database
echo "Populating test data..."
psql -U postgres -d test-cinch-dev -f /app/scripts/seed_test_data.sql || { echo "Failed to populate test-cinch-dev data"; exit 1; }

echo "Database initialization completed successfully" 