import logging


# Database settings
SQLALCHEMY_DATABASE_URI = 'postgresql://kinderstadt@localhost/kinderstadt_passgen'

# Celery settings
CELERY_BROKER_URL = 'amqp://guest:guest@localhost/'
CELERYD_LOG_LEVEL = 'INFO'

# App specific settings
PASSGEN_LOG_LEVEL = logging.INFO
