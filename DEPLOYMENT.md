# Deployment Guide

This guide explains how to deploy the Team ZAC Scheduler application using the refactored architecture.

## Prerequisites

- Python 3.8+
- Redis server
- Nginx
- Gunicorn
- PostgreSQL (optional, SQLite is default)

## Installation Steps

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Set Environment Variables

Create a `.env` file:

```bash
SECRET_KEY=your-secret-key-here
DATABASE_URL=sqlite:///instance/database.db
REDIS_URL=redis://localhost:6379/0
CELERY_BROKER_URL=redis://localhost:6379/0
CELERY_RESULT_BACKEND=redis://localhost:6379/0
```

### 3. Initialize Database with Flask-Migrate

```bash
flask db init
flask db migrate -m "Initial migration"
flask db upgrade
```

### 4. Start Redis

```bash
# On Linux/Mac
redis-server

# On Windows, use Redis for Windows or WSL
```

### 5. Start Celery Worker (for background tasks)

```bash
celery -A app.celery_worker.celery worker --loglevel=info
```

### 6. Start Gunicorn Server

```bash
gunicorn -c gunicorn_config.py run:app
```

Or with more workers:

```bash
gunicorn -w 4 -b 0.0.0.0:8000 run:app
```

### 7. Configure Nginx

1. Copy `nginx.conf` to `/etc/nginx/sites-available/team-zac-scheduler`
2. Update paths and domain name in the config file
3. Create symlink:
   ```bash
   sudo ln -s /etc/nginx/sites-available/team-zac-scheduler /etc/nginx/sites-enabled/
   ```
4. Test and reload Nginx:
   ```bash
   sudo nginx -t
   sudo systemctl reload nginx
   ```

## Systemd Service Files

### Gunicorn Service (`/etc/systemd/system/team-zac-scheduler.service`)

```ini
[Unit]
Description=Team ZAC Scheduler Gunicorn daemon
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/path/to/TEAM-ZAC-SCHEDULER
Environment="PATH=/path/to/venv/bin"
ExecStart=/path/to/venv/bin/gunicorn -c gunicorn_config.py run:app

[Install]
WantedBy=multi-user.target
```

### Celery Worker Service (`/etc/systemd/system/team-zac-celery.service`)

```ini
[Unit]
Description=Team ZAC Scheduler Celery Worker
After=network.target redis.service

[Service]
Type=forking
User=www-data
Group=www-data
WorkingDirectory=/path/to/TEAM-ZAC-SCHEDULER
Environment="PATH=/path/to/venv/bin"
ExecStart=/path/to/venv/bin/celery -A app.celery_worker.celery worker --loglevel=info --detach
ExecStop=/bin/kill -s TERM $MAINPID

[Install]
WantedBy=multi-user.target
```

Enable and start services:

```bash
sudo systemctl enable team-zac-scheduler.service
sudo systemctl enable team-zac-celery.service
sudo systemctl start team-zac-scheduler.service
sudo systemctl start team-zac-celery.service
```

## Development Mode

For development, you can still use:

```bash
python run.py
```

## Monitoring

- Check Gunicorn status: `sudo systemctl status team-zac-scheduler`
- Check Celery status: `sudo systemctl status team-zac-celery`
- View logs: `journalctl -u team-zac-scheduler -f`

