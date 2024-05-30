from flask import Blueprint, jsonify, request
from app import models as m, db


product_blueprint = Blueprint("product", __name__)


@product_blueprint.route("/<int:product_id>", methods=["GET"])
def get_product_by_id(product_id: int) -> m.Product:
    product_query = m.Product.select().where(m.Product.id == product_id)
    product: m.Product = db.session.scalar(product_query)
    return jsonify(product)