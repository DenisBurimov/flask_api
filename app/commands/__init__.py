import click
from flask import Flask


def init(app: Flask):
    @app.cli.command("parse-csv")
    @click.option("--path", type=str)
    def parse_csv(path: str):
        from app.controllers import parse_csv

        parse_csv(path)
        click.echo("CSV parsed successfully")
