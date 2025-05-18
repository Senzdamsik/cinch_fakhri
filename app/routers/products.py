from collections.abc import Sequence
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Path, Query
from pydantic import BaseModel, ConfigDict
from sqlalchemy import select
from sqlalchemy.orm import Session, joinedload

from app.db.database import get_db
from app.models.models import Attribute, Product, ProductPricing, Region, RentalPeriod

router = APIRouter(prefix="/products", tags=["products"])

# Dependency
db_dependency = Depends(get_db)


class AttributeValueResponse(BaseModel):
    """Response model for attribute values.

    Attributes:
        id (int): The unique identifier of the attribute value.
        value (str): The actual value of the attribute.
    """

    model_config = ConfigDict(from_attributes=True)

    id: int
    value: str


class AttributeResponse(BaseModel):
    """Response model for product attribute information.

    Attributes:
        id (int): The unique identifier of the attribute.
        name (str): The name of the attribute.
        values (Sequence[AttributeValueResponse]): List of possible values for
            this attribute.
    """

    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    values: Sequence[AttributeValueResponse]


class PricingResponse(BaseModel):
    """Response model for product pricing information.

    Attributes:
        rental_period (int): Duration of the rental period in months.
        region (str): Name of the region where this pricing applies.
        price (float): The price for this rental period and region combination.
    """

    model_config = ConfigDict(from_attributes=True)

    rental_period: int
    region: str
    price: float


class ProductResponse(BaseModel):
    """Response model for detailed product information.

    Attributes:
        id (int): The unique identifier of the product.
        name (str): The name of the product.
        description (str): Detailed description of the product.
        sku (str): Stock keeping unit, unique identifier for the product.
        attributes (Sequence[AttributeResponse]): List of product attributes.
        pricings (Sequence[PricingResponse]): List of pricing information.
    """

    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    description: str
    sku: str
    attributes: Sequence[AttributeResponse]
    pricings: Sequence[PricingResponse]


class ProductListResponse(BaseModel):
    """Response model for paginated product listings.

    Attributes:
        items (Sequence[ProductResponse]): List of products.
        total (int): Total number of products matching the filter criteria.
    """

    model_config = ConfigDict(from_attributes=True)

    items: Sequence[ProductResponse]
    total: int


@router.get("/{product_id}", response_model=ProductResponse)
async def get_product(
    product_id: Annotated[int, Path(
        description="The ID of the product to retrieve",
        examples=[1],
        ge=1
    )],
    db: Session = db_dependency,
    attributes_page: Annotated[int, Query(
        ge=1,
        description="Page number for attributes pagination",
        examples=[1]
    )] = 1,
    attributes_per_page: Annotated[int, Query(
        ge=1,
        description="Number of attributes per page",
        examples=[10]
    )] = 10,
) -> ProductResponse:
    # Optimized query with eager loading and pagination
    stmt = (
        select(Product)
        .options(
            joinedload(Product.attributes).joinedload(Attribute.values),
            joinedload(Product.pricings).joinedload(ProductPricing.rental_period),
            joinedload(Product.pricings).joinedload(ProductPricing.region),
        )
        .filter(Product.id == product_id)
    )
    product = db.execute(stmt).scalars().first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    # Paginate attributes
    start = (attributes_page - 1) * attributes_per_page
    end = start + attributes_per_page
    paginated_attributes = product.attributes[start:end]

    return ProductResponse(
        id=product.id,
        name=product.name,
        description=product.description,
        sku=product.sku,
        attributes=[
            AttributeResponse(
                id=attr.id,
                name=attr.name,
                values=[
                    AttributeValueResponse(id=val.id, value=val.value)
                    for val in attr.values
                ],
            )
            for attr in paginated_attributes
        ],
        pricings=[
            PricingResponse(
                rental_period=pricing.rental_period.duration_months,
                region=pricing.region.name,
                price=pricing.price,
            )
            for pricing in product.pricings
        ],
    )


@router.get("", response_model=ProductListResponse)
async def list_products(
    db: Session = db_dependency,
    region: Annotated[str | None, Query(
        description="Filter products by region name (example: 'Singapore', 'Malaysia')",
        examples=["Singapore", "Malaysia"]
    )] = None,
    rental_period: Annotated[int | None, Query(
        description="Filter by rental period duration in months",
        examples=[3, 6, 12]
    )] = None,
    page: Annotated[int, Query(
        ge=1,
        description="Page number for pagination of results",
        examples=[1]
    )] = 1,
    per_page: Annotated[int, Query(
        ge=1,
        le=100,
        description="Number of items to return per page (max 100)",
        examples=[10, 20, 50]
    )] = 10,
) -> ProductListResponse:
    # Start with base query
    stmt = select(Product).options(
        joinedload(Product.attributes).joinedload(Attribute.values),
        joinedload(Product.pricings).joinedload(ProductPricing.rental_period),
        joinedload(Product.pricings).joinedload(ProductPricing.region),
    )

    # Apply filters if provided
    filters_applied = False

    if region is not None:
        if not filters_applied:
            stmt = stmt.join(ProductPricing)
            filters_applied = True
        stmt = stmt.join(Region).filter(Region.name == region)

    if rental_period is not None:
        if not filters_applied:
            stmt = stmt.join(ProductPricing)
        stmt = stmt.join(RentalPeriod).filter(
            RentalPeriod.duration_months == rental_period
        )

    # Get total count for pagination
    count_stmt = select(Product)
    if filters_applied:
        count_stmt = count_stmt.join(ProductPricing)
        if region is not None:
            count_stmt = count_stmt.join(Region).filter(Region.name == region)
        if rental_period is not None:
            count_stmt = count_stmt.join(RentalPeriod).filter(
                RentalPeriod.duration_months == rental_period
            )
    total = len(db.scalars(count_stmt).unique().all())

    # Apply pagination
    offset = (page - 1) * per_page
    stmt = stmt.offset(offset).limit(per_page)
    products = db.scalars(stmt).unique().all()

    return ProductListResponse(
        items=[
            ProductResponse(
                id=product.id,
                name=product.name,
                description=product.description,
                sku=product.sku,
                attributes=[
                    AttributeResponse(
                        id=attr.id,
                        name=attr.name,
                        values=[
                            AttributeValueResponse(id=val.id, value=val.value)
                            for val in attr.values
                        ],
                    )
                    for attr in product.attributes
                ],
                pricings=[
                    PricingResponse(
                        rental_period=pricing.rental_period.duration_months,
                        region=pricing.region.name,
                        price=pricing.price,
                    )
                    for pricing in product.pricings
                ],
            )
            for product in products
        ],
        total=total,
    )
