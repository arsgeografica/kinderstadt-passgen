import logging
from path import Path


_BASE_DIR = Path(__file__).abspath().dirname().dirname()

SECRET_KEY = '5m34a58x(3^$np08v!si#!a1btp$(h$a0qa-j_c)^!-ah=ypqs'

# Celery settings
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERYD_CONCURRENCY = 2

# App specific settings
ID_ENCODE_OFFSET = 10000
RANGE_SIZE_MAX = 50
PASSGEN_LOG_LEVEL = logging.WARN

FILE_STORAGE_PATH = _BASE_DIR / '../media'

# PDF settings
COVER_PDF = _BASE_DIR / 'templates/cover.pdf'
PASS_NUP = 4
AGREEMENT_NUP = 1
