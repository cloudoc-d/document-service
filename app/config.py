import os


class Config:
    MONGODB_URL = os.getenv('MONGODB_URL')
    BROADCAST_STORAGE_URL = os.getenv('BROADCAST_STORAGE_URL', 'memory://')

    CELERY_BROKER_URL = os.getenv('CELERY_BROKER_URL')
    CELERY_RESULT_BACKEND = os.getenv('CELERY_RESULT_BACKEND')

    REDIS_STORAGE_URL = os.getenv('REDIS_STORAGE_URL')
