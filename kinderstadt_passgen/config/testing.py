import tempfile
from kinderstadt_passgen.config.development import *

CELERY_ALWAYS_EAGER = True

FILE_STORAGE_PATH = tempfile.mkdtemp(suffix='passgen_test')
