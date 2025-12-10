"""
Celery configuration for background tasks
"""
from app import create_app
from celery import Celery
from config import Config

def make_celery(app):
    """Create and configure Celery app"""
    celery = Celery(
        app.import_name,
        backend=app.config['CELERY_RESULT_BACKEND'],
        broker=app.config['CELERY_BROKER_URL']
    )
    celery.conf.update(app.config)
    
    class ContextTask(celery.Task):
        """Make celery tasks work with Flask app context"""
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)
    
    celery.Task = ContextTask
    return celery

# Create Flask app and Celery instance
flask_app = create_app()
celery = make_celery(flask_app)

# Import tasks to register them
# from app.tasks import sms_tasks  # Will be created

