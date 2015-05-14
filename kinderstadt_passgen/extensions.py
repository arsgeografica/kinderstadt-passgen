from flask.ext.celery import Celery
from flask.ext.marshmallow import Marshmallow
from flask.ext.migrate import Migrate
from flask.ext.sqlalchemy import SQLAlchemy

db = SQLAlchemy()
celery = Celery()
ma = Marshmallow()
migrate = Migrate()
