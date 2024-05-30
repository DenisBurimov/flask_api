from typing import TYPE_CHECKING
import sqlalchemy as sa
from sqlalchemy import orm
from app import db
from .utils import ModelMixin


if TYPE_CHECKING:
    from .product import Product


class Review(db.Model, ModelMixin):
    __tablename__ = "reviews"

    id: orm.Mapped[int] = orm.mapped_column(primary_key=True)
    title: orm.Mapped[str] = orm.mapped_column(sa.String(255))
    review: orm.Mapped[str] = orm.mapped_column(sa.Text)

    # Foregin Keys
    product_id: orm.Mapped[int] = orm.mapped_column(sa.ForeignKey("products.id"))

    # Relationships
    product: orm.Mapped["Product"] = orm.relationship(back_populates="reviews")

    def __repr__(self) -> str:
        return f"<Review {self.title} of product: {self.product_id}>"
