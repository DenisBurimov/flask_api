from flask import Blueprint, jsonify
from app import db, models as m, schema as s


product_blueprint = Blueprint("product", __name__)


@product_blueprint.route("/<int:product_id>", methods=["GET"])
def get_product_by_id(product_id: int) -> m.Product:
    product_query = m.Product.select().where(m.Product.id == product_id)
    product: m.Product = db.session.scalar(product_query)

    # Output validation with Pydantic
    result = s.ProductGetOutput.model_validate(product)
    return jsonify(result.model_dump())
