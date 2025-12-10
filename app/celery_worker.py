"""
Celery worker startup script
Run with: celery -A celery_app.celery worker --loglevel=info
"""
from celery_app import celery

if __name__ == '__main__':
    celery.worker_main()

