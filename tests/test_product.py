from flask.testing import FlaskClient, FlaskCliRunner
from click.testing import Result
from app import models as m, db
from app.controllers import parse_csv


def test_get_product(client: FlaskClient):
    parse_csv()
    product: m.Product = db.session.scalar(m.Product.select())

    response = client.get(f"/{product.id}")
    assert response.status_code == 200
    assert response.json["asin"] == product.asin
    assert response.json["title"] == product.title


def test_parse_csv(client: FlaskClient):
    parse_csv()
    products_count = db.session.query(m.Product).count()
    assert products_count == 11

    reviews_count = db.session.query(m.Review).count()
    assert reviews_count == 27


def test_parse_command(runner: FlaskCliRunner):
    result: Result = runner.invoke(args=["parse-csv"])

    assert "CSV parsed successfully" in result.output
