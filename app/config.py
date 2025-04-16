import os


class Config:
    MONGODB_URL = os.getenv('MONGODB_URL')
    BROADCAST_STORAGE_URL = os.getenv('BROADCAST_STORAGE_URL', 'memory://')
