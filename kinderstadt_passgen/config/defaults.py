# Celery settings
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_IMPORTS = ('kinderstadt_passgen.tasks',)

# App specific settings
ID_ENCODE_OFFSET = 10000
