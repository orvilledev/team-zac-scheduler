"""
Gunicorn configuration file
"""
import multiprocessing
import os

# Server socket
# Render provides PORT environment variable, default to 8000 for local development
port = int(os.environ.get('PORT', 8000))
bind = f'0.0.0.0:{port}'
backlog = 2048

# Worker processes
workers = int(os.environ.get('GUNICORN_WORKERS', multiprocessing.cpu_count() * 2 + 1))
worker_class = 'sync'
worker_connections = 1000
timeout = 30
keepalive = 2

# Logging
accesslog = '-'
errorlog = '-'
loglevel = os.environ.get('GUNICORN_LOG_LEVEL', 'info')
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s" %(D)s'

# Process naming
proc_name = 'team-zac-scheduler'

# Server mechanics
daemon = False
pidfile = '/tmp/gunicorn.pid'
umask = 0
user = None
group = None
tmp_upload_dir = None

# SSL (if needed)
# keyfile = '/path/to/keyfile'
# certfile = '/path/to/certfile'

# Performance
preload_app = True
max_requests = 1000
max_requests_jitter = 50

def on_starting(server):
    """Called just before the master process is initialized."""
    server.log.info("Starting Team ZAC Scheduler server")

def when_ready(server):
    """Called just after the server is started."""
    server.log.info("Server is ready. Spawning workers")

def on_exit(server):
    """Called just before exiting Gunicorn."""
    server.log.info("Shutting down: Team ZAC Scheduler")

