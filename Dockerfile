FROM python:3.10-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    netcat-openbsd \
    && rm -rf /var/lib/apt/lists/*

COPY pyproject.toml ./
COPY app ./app
COPY alembic ./alembic
COPY alembic.ini ./

RUN pip install --no-cache-dir \
    fastapi==0.110.0 \
    uvicorn==0.27.1 \
    sqlalchemy==2.0.28 \
    alembic==1.13.1 \
    psycopg2==2.9.9 \
    pytest==8.2.0 \
    pytest-asyncio==0.26.0 \
    httpx==0.27.0 \
    python-dotenv==1.0.1 \
    pydantic-settings==2.2.1

EXPOSE 8000

CMD ["sh", "-c", "alembic upgrade head && uvicorn app.main:app --host 0.0.0.0 --port 8000"]