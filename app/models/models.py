from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import Float, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, relationship
from sqlalchemy.orm.decl_api import mapped_column  # type: ignore

from app.db.database import Base

if TYPE_CHECKING:
    from typing import TypeAlias

    Product_t: TypeAlias = "Product"
    Attribute_t: TypeAlias = "Attribute"
    AttributeValue_t: TypeAlias = "AttributeValue"
    RentalPeriod_t: TypeAlias = "RentalPeriod"
    Region_t: TypeAlias = "Region"
    ProductPricing_t: TypeAlias = "ProductPricing"


class Product(Base):
    """Product model representing items available for rental.

    Attributes:
        id (int): Primary key for the product.
        name (str): Name of the product.
        description (str): Detailed description of the product.
        sku (str): Stock keeping unit, unique identifier for the product.
        attributes (List[Attribute]): List of product attributes.
        pricings (List[ProductPricing]): List of product pricing information.
    """

    __tablename__ = "products"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String, index=True)
    description: Mapped[str] = mapped_column(String)
    sku: Mapped[str] = mapped_column(String, unique=True, index=True)

    attributes: Mapped[list[Attribute]] = relationship(
        "Attribute", back_populates="product"
    )
    pricings: Mapped[list[ProductPricing]] = relationship(
        "ProductPricing", back_populates="product"
    )


class Attribute(Base):
    """Product attribute model.

    Attributes:
        id (int): Primary key for the attribute.
        product_id (int): Foreign key referencing the product.
        name (str): Name of the attribute.
        product (Product): Related product.
        values (List[AttributeValue]): List of possible values for this attribute.
    """

    __tablename__ = "attributes"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    product_id: Mapped[int] = mapped_column(Integer, ForeignKey("products.id"))
    name: Mapped[str] = mapped_column(String)

    product: Mapped[Product] = relationship("Product", back_populates="attributes")
    values: Mapped[list[AttributeValue]] = relationship(
        "AttributeValue", back_populates="attribute"
    )


class AttributeValue(Base):
    """Value for a product attribute.

    Attributes:
        id (int): Primary key for the attribute value.
        attribute_id (int): Foreign key referencing the attribute.
        value (str): The actual value of the attribute.
        attribute (Attribute): Related attribute.
    """

    __tablename__ = "attribute_values"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    attribute_id: Mapped[int] = mapped_column(Integer, ForeignKey("attributes.id"))
    value: Mapped[str] = mapped_column(String)

    attribute: Mapped[Attribute] = relationship("Attribute", back_populates="values")


class RentalPeriod(Base):
    """Rental period model defining available durations.

    Attributes:
        id (int): Primary key for the rental period.
        duration_months (int): Duration of the rental period in months.
        pricings (List[ProductPricing]): List of product prices for this period.
    """

    __tablename__ = "rental_periods"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    duration_months: Mapped[int] = mapped_column(Integer, unique=True)

    pricings: Mapped[list[ProductPricing]] = relationship(
        "ProductPricing", back_populates="rental_period"
    )


class Region(Base):
    """Region model representing different geographical areas.

    Attributes:
        id (int): Primary key for the region.
        name (str): Name of the region.
        pricings (List[ProductPricing]): List of product prices for this region.
    """

    __tablename__ = "regions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String, unique=True)

    pricings: Mapped[list[ProductPricing]] = relationship(
        "ProductPricing", back_populates="region"
    )


class ProductPricing(Base):
    """Product pricing model for different regions and rental periods.

    Attributes:
        id (int): Primary key for the pricing.
        product_id (int): Foreign key referencing the product.
        rental_period_id (int): Foreign key referencing the rental period.
        region_id (int): Foreign key referencing the region.
        price (float): Price for the product in this configuration.
        product (Product): Related product.
        rental_period (RentalPeriod): Related rental period.
        region (Region): Related region.
    """

    __tablename__ = "product_pricings"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    product_id: Mapped[int] = mapped_column(Integer, ForeignKey("products.id"))
    rental_period_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("rental_periods.id")
    )
    region_id: Mapped[int] = mapped_column(Integer, ForeignKey("regions.id"))
    price: Mapped[float] = mapped_column(Float)

    product: Mapped[Product] = relationship("Product", back_populates="pricings")
    rental_period: Mapped[RentalPeriod] = relationship(
        "RentalPeriod", back_populates="pricings"
    )
    region: Mapped[Region] = relationship("Region", back_populates="pricings")
