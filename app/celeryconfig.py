from celery import Celery
from config import REDIS_URL

celery = Celery(__name__)

celery.conf.broker_url = REDIS_URL

