from flask.ext.celery import Celery
from flask.ext.migrate import Migrate
from flask.ext.sqlalchemy import SQLAlchemy

db = SQLAlchemy()
celery = Celery()
migrate = Migrate()
