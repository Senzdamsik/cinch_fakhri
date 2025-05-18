"""Create initial tables.

Revision ID: 6dec139d40e4
Revises: None
Create Date: 2024-03-14
"""

from __future__ import annotations

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op  # type: ignore

# revision identifiers, used by Alembic
revision: str = "6dec139d40e4"
down_revision: str | None = None
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Create all initial tables."""
    # Create products table
    op.create_table(
        "products",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(), nullable=True),
        sa.Column("description", sa.String(), nullable=True),
        sa.Column("sku", sa.String(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_products_id"), "products", ["id"], unique=False)
    op.create_index(op.f("ix_products_name"), "products", ["name"], unique=False)
    op.create_index(op.f("ix_products_sku"), "products", ["sku"], unique=True)

    # Create regions table
    op.create_table(
        "regions",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("name"),
    )
    op.create_index(op.f("ix_regions_id"), "regions", ["id"], unique=False)

    # Create rental_periods table
    op.create_table(
        "rental_periods",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("duration_months", sa.Integer(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("duration_months"),
    )
    op.create_index(
        op.f("ix_rental_periods_id"), "rental_periods", ["id"], unique=False
    )

    # Create attributes table
    op.create_table(
        "attributes",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("product_id", sa.Integer(), nullable=True),
        sa.Column("name", sa.String(), nullable=True),
        sa.ForeignKeyConstraint(
            ["product_id"],
            ["products.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_attributes_id"), "attributes", ["id"], unique=False)

    # Create product_pricings table
    op.create_table(
        "product_pricings",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("product_id", sa.Integer(), nullable=True),
        sa.Column("rental_period_id", sa.Integer(), nullable=True),
        sa.Column("region_id", sa.Integer(), nullable=True),
        sa.Column("price", sa.Float(), nullable=True),
        sa.ForeignKeyConstraint(
            ["product_id"],
            ["products.id"],
        ),
        sa.ForeignKeyConstraint(
            ["region_id"],
            ["regions.id"],
        ),
        sa.ForeignKeyConstraint(
            ["rental_period_id"],
            ["rental_periods.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_product_pricings_id"), "product_pricings", ["id"], unique=False
    )

    # Create attribute_values table
    op.create_table(
        "attribute_values",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("attribute_id", sa.Integer(), nullable=True),
        sa.Column("value", sa.String(), nullable=True),
        sa.ForeignKeyConstraint(
            ["attribute_id"],
            ["attributes.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_attribute_values_id"), "attribute_values", ["id"], unique=False
    )


def downgrade() -> None:
    """Revert all migrations."""
    op.drop_index(op.f("ix_attribute_values_id"), table_name="attribute_values")
    op.drop_table("attribute_values")
    op.drop_index(op.f("ix_product_pricings_id"), table_name="product_pricings")
    op.drop_table("product_pricings")
    op.drop_index(op.f("ix_attributes_id"), table_name="attributes")
    op.drop_table("attributes")
    op.drop_index(op.f("ix_rental_periods_id"), table_name="rental_periods")
    op.drop_table("rental_periods")
    op.drop_index(op.f("ix_regions_id"), table_name="regions")
    op.drop_table("regions")
    op.drop_index(op.f("ix_products_sku"), table_name="products")
    op.drop_index(op.f("ix_products_name"), table_name="products")
    op.drop_index(op.f("ix_products_id"), table_name="products")
    op.drop_table("products")
