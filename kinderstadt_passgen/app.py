from flask import Flask
from kinderstadt_passgen.models import db
from kinderstadt_passgen import views
from kinderstadt_passgen.tasks import celery


def factory(config=None):
    app = Flask(__name__.split('.')[0])
    app.config.from_object('kinderstadt_passgen.config.defaults')
    if config:
        app.config.from_object(config)

    db.init_app(app)
    celery.init_app(app)

    from pprint import pprint
    pprint(celery.conf)

    app.add_url_rule('/', 'home', views.home)
    app.add_url_rule('/order', 'order_create', views.order, methods=('POST',))
    app.add_url_rule('/order/<id>', 'order', views.order)
    app.add_url_rule('/order/<id>/download', 'download', views.download)

    return app
