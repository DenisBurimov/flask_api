from typing import TYPE_CHECKING
import sqlalchemy as sa
from sqlalchemy import orm
from app import db
from .utils import ModelMixin


if TYPE_CHECKING:
    from .review import Review


class Product(db.Model, ModelMixin):
    __tablename__ = "products"

    id: orm.Mapped[int] = orm.mapped_column(primary_key=True)
    title: orm.Mapped[str] = orm.mapped_column(sa.String(255))
    asin: orm.Mapped[str] = orm.mapped_column(sa.String(16))

    # Relationships
    reviews: orm.Mapped[list["Review"]] = orm.relationship(back_populates="product")

    def __repr__(self) -> str:
        return f"<Product {self.asin}>"
