import click
from flask import Flask


def init(app: Flask):
    @app.cli.command("parse-csv")
    @click.option("--products_file", type=str)
    @click.option("--reviews_file", type=str)
    def parse_csv(products_file: str, reviews_file: str):
        from app.controllers import parse_csv

        parse_csv()
        click.echo("CSV parsed successfully")
