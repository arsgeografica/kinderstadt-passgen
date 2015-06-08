import pytest
from flask.ext import migrate as migrate_extension
import testing.postgresql
from kinderstadt_passgen.app import factory


@pytest.fixture(scope="session")
def app(request):
    # Create PostgreSQL server on the fly
    postgresql = testing.postgresql.Postgresql()

    # And override the database URL
    app = factory('kinderstadt_passgen.config.development')
    app.config['SQLALCHEMY_DATABASE_URI'] = postgresql.url()

    # Set up schema
    with app.app_context():
        migrate_extension.upgrade(revision='head')

    def fin():
        postgresql.stop()

    request.addfinalizer(fin)

    return app
