"""
APScheduler initialization for background tasks
"""
import os
import atexit
from apscheduler.schedulers.background import BackgroundScheduler

scheduler = None

def init_scheduler(app):
    """Initialize APScheduler if not in debug mode or main process"""
    global scheduler
    
    if not app.debug or os.environ.get('WERKZEUG_RUN_MAIN') == 'true':
        try:
            scheduler = BackgroundScheduler()
            if not scheduler.running:
                scheduler.start()
            atexit.register(lambda: scheduler.shutdown() if scheduler and scheduler.running else None)
        except Exception as e:
            print(f"Warning: Could not start scheduler: {e}")
            scheduler = None
    
    return scheduler

def get_scheduler():
    """Get the global scheduler instance"""
    return scheduler

