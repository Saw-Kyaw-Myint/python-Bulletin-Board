from celery import Celery
from flask import Flask

from config.celery import CeleryConfig

celery = Celery(__name__)


def celery_init_app(app: Flask):
    celery.conf.broker_url = CeleryConfig.CELERY_BROKER_URL
    celery.conf.result_backend = CeleryConfig.CELERY_RESULT_BACKEND
    celery.conf.task_ignore_result = CeleryConfig.CELERY_TASK_IGNORE_RESULT

    celery.set_default()
    return celery
