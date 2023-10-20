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



