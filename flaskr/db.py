"""
Model - Database logic  goes here
"""
import sqlite3

import click
from flask import current_app,g

def get_db():
    """ function to connect to the database """
    
    if "db" not in g:
        g.db = sqlite3.connect(
            current_app.config["DATABASE"],
            detect_types = sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row
    return g.db

#closing an opended db

def close_db(e=None):
    db=g.pop("db",None)

    if db is not None:
        db.close()

def init_db():
    db = get_db()

    with current_app.open_resource("schema.sql") as f:
        db.executescript(f.read().decode("utf8"))

@click.command("init-db")
def init_db_command():
    init_db()
    click.echo("initialized the database...")


def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)

