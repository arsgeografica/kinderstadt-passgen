import os.path
from flask import Flask
from kinderstadt_passgen.extensions import db, celery, migrate
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

    app.add_url_rule('/', 'home', views.home)
    app.add_url_rule('/order', 'order_create', views.order, methods=('POST',))
    app.add_url_rule('/order/<base62_id>', 'order', views.order)
    app.add_url_rule('/order/<base62_id>/download', 'download', views.download)

    return app
