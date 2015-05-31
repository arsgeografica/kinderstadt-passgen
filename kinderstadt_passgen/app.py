import logging
import os.path
from flask import Flask
from kinderstadt_passgen.extensions import db, celery, ma, migrate
from kinderstadt_passgen import views


def factory(config=None):
    app = Flask(__name__.split('.')[0])
    app.config.from_object('kinderstadt_passgen.config.defaults')
    if config:
        app.config.from_object(config)

    db.init_app(app)
    migrations_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                  'migrations')
    migrate.init_app(app, db, directory=migrations_dir)
    celery.init_app(app)
    ma.init_app(app)

    app.add_url_rule('/', 'home', views.home)
    app.add_url_rule('/order', 'order_create', views.order,
                     methods=('GET', 'POST'))
    app.add_url_rule('/order/<base62_id>', 'order', views.order)
    app.add_url_rule('/order/<base62_id>.pdf', 'download', views.download)

    logger = logging.getLogger(app.name)
    logger.setLevel(app.config['PASSGEN_LOG_LEVEL'])

    return app
