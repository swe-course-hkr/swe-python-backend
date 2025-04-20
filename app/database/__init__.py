"""
creates the SQLAlchemy object for ORM integration with flask.

`db` will define models and manage database operations.
"""

from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()