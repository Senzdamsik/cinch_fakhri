from __future__ import annotations

import os
from logging.config import fileConfig

from dotenv import load_dotenv
from sqlalchemy import engine_from_config
from sqlalchemy.pool import NullPool

from alembic import context  # type: ignore
from app.db.database import Base
from app.models.models import *  # noqa: F403

load_dotenv()

config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

database_url = os.getenv("DATABASE_URL")
if database_url is None:
    raise ValueError("DATABASE_URL environment variable is not set")
config.set_main_option("sqlalchemy.url", database_url)

target_metadata = Base.metadata

section = config.get_section(config.config_ini_section)
if section is None:
    raise ValueError(f"Config section {config.config_ini_section} not found")

connectable = engine_from_config(
    section,
    prefix="sqlalchemy.",
    poolclass=NullPool,
)

with connectable.connect() as connection:
    context.configure(
        connection=connection,
        target_metadata=target_metadata,
    )
    with context.begin_transaction():
        context.run_migrations()
