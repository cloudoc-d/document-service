from celery import Celery
from app.config import Config
from renderer_definition.tasks import render_pdf_task

import os


celery_app = Celery(
    'document-service',
    broker=Config.CELERY_BROKER_URL,
    backend=Config.CELERY_RESULT_BACKEND,
)

celery_app.register_task(render_pdf_task)
