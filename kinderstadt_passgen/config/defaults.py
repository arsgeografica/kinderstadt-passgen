from path import Path


_BASE_DIR = Path(__file__).abspath().dirname().dirname()

# Celery settings
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'

# App specific settings
ID_ENCODE_OFFSET = 10000

FILE_STORAGE_PATH = _BASE_DIR / '../media'
