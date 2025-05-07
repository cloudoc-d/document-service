import os


class Config:
    MONGODB_URL = os.getenv('MONGODB_URL', 'mongodb://localhost:27017/')
    BROADCAST_STORAGE_URL = os.getenv('BROADCAST_STORAGE_URL', 'redis://127.0.0.1:6379/')

    CELERY_BROKER_URL = os.getenv('CELERY_BROKER_URL', 'amqp://guest:guest@localhost:5672//')
    CELERY_RESULT_BACKEND = os.getenv('CELERY_RESULT_BACKEND', 'redis://locahost:6379/')

    REDIS_STORAGE_URL = os.getenv('REDIS_STORAGE_URL', 'redis://127.0.0.1:6379/')

    DATABASE_NAME = 'cloudoc'
