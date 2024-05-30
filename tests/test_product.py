from flask.testing import FlaskClient, FlaskCliRunner
from click.testing import Result
from app import models as m, db


def test_get_product(client: FlaskClient):
    response = client.get("/1")
    assert response.status_code == 200
    assert response


"""
def test_create_admin(runner: FlaskCliRunner):
    res: Result = runner.invoke(args=["create-admin"])
"""


def test_parse_csv(client: FlaskClient):
    from app.controllers import parse_csv

    parse_csv()
    products_count = db.session.query(m.Product).count()
    assert products_count == 11

    reviews_count = db.session.query(m.Review).count()
    assert reviews_count == 27


def test_parse_command(runner: FlaskCliRunner):
    result: Result = runner.invoke(
        args=["parse-csv", "--path=tests/db/Products_Reviews-Products.csv"]
    )

    assert "CSV parsed successfully" in result.output

    result: Result = runner.invoke(
        args=["parse-csv", "--path=tests/db/Products_Reviews-Reviews.csv"]
    )

    assert "CSV parsed successfully" in result.output
