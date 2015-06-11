import logging
import sys
from path import Path
from kombu import Exchange, Queue


_BASE_DIR = Path(__file__).abspath().dirname().dirname()

SECRET_KEY = '5m34a58x(3^$np08v!si#!a1btp$(h$a0qa-j_c)^!-ah=ypqs'

# Database settings
SQLALCHEMY_DATABASE_URI = 'postgresql://kinderstadt@localhost/passgen'

# Celery settings
CELERY_BROKER_URL = 'amqp://kinderstadt:kinderstadt@localhost/passgen'
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERYD_CONCURRENCY = 2


CELERY_QUEUES = (
    Queue('passgen',
          Exchange('passgen', type='topic'),
          routing_key='kinderstadt.passgen'),
)

CELERY_ROUTES = ({
    'passgen.tasks.execute_order': {
        'queue': 'passgen',
        'routing_key': 'kinderstadt.passgen'
    }
},)

# App specific settings
ID_ENCODE_OFFSET = 10000
RANGE_SIZE_DEFAULT = 3
RANGE_SIZE_MAX = 50
FILE_STORAGE_PATH = _BASE_DIR / '../media'
CLEANUP_WAIT_HOURS = 1

LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
LOG_LEVEL = logging.INFO
LOG_FILE = _BASE_DIR / '../passgen.log'
LOG_FILE_MAX_BYTES = 10 * 1024*1024
LOG_FILE_BACKUP_COUNT = 5
LOG_FILE_LOG_LEVEL = LOG_LEVEL

# PDF settings
COVER_PDF = _BASE_DIR / 'templates/cover.pdf'
PASS_NUP = 4
AGREEMENT_NUP = 1
