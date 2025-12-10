# Deploying to Render

This guide will help you deploy the Team ZAC Scheduler application to Render.

## Prerequisites

1. A GitHub account
2. A Render account (sign up at https://render.com)
3. Your code pushed to a GitHub repository

## Deployment Steps

### Option 1: Using render.yaml (Recommended)

1. **Push your code to GitHub** (make sure all files are committed)

2. **Go to Render Dashboard** → New → Blueprint

3. **Connect your GitHub repository**

4. **Render will automatically detect `render.yaml`** and create the services

5. **Set Environment Variables** in the Render dashboard:
   - `SECRET_KEY` - Generate a strong secret key (Render can auto-generate this)
   - `REDIS_URL` - (Optional) If you're using Redis
   - `CELERY_BROKER_URL` - (Optional) If you're using Celery
   - `CELERY_RESULT_BACKEND` - (Optional) If you're using Celery

6. **Deploy** - Render will automatically build and deploy your application

### Option 2: Manual Setup

1. **Create a PostgreSQL Database**:
   - Go to Render Dashboard → New → PostgreSQL
   - Choose a name (e.g., `team-zac-db`)
   - Select the free plan
   - Note the connection string

2. **Create a Web Service**:
   - Go to Render Dashboard → New → Web Service
   - Connect your GitHub repository
   - Configure:
     - **Name**: `team-zac-scheduler`
     - **Environment**: `Python 3`
     - **Build Command**: `pip install -r requirements.txt`
     - **Start Command**: `gunicorn -c gunicorn_config.py app:app`
     - **Plan**: Free (or choose a paid plan)

3. **Set Environment Variables**:
   - `DATABASE_URL` - From your PostgreSQL database (Render auto-provides this if linked)
   - `SECRET_KEY` - Generate a strong secret key

4. **Link the Database**:
   - In your Web Service settings, go to "Environment"
   - Link your PostgreSQL database
   - Render will automatically set `DATABASE_URL`

5. **Deploy** - Click "Create Web Service"

## Post-Deployment

1. **Initialize the Database**:
   - After first deployment, open Render's Shell (in your web service dashboard)
   - Run: `python init_render_db.py`
   - This will create all database tables and a default admin user

2. **Create Admin User** (if needed):
   - If you need to create a custom admin user, use Render's Shell
   - Run: `python create_admin.py`
   - Follow the prompts to create your admin account

3. **Access Your App**:
   - Render will provide a URL like `https://your-app-name.onrender.com`
   - Share this URL with your team

## Important Notes

- **Free Tier Limitations**: 
  - Render's free tier spins down after 15 minutes of inactivity
  - First request after spin-down may take 30-60 seconds
  - Consider upgrading to a paid plan for production use

- **File Storage**:
  - Uploaded files are stored in the filesystem
  - On free tier, files may be lost during redeployments
  - Consider using cloud storage (AWS S3, Cloudinary) for production

- **Database**:
  - PostgreSQL database is persistent
  - Free tier has 90-day data retention
  - Backup your database regularly

- **Environment Variables**:
  - Never commit sensitive data to GitHub
  - Always use environment variables for secrets
  - Render provides secure environment variable storage

## Troubleshooting

- **Build Fails**: Check the build logs in Render dashboard
- **App Crashes**: Check the runtime logs
- **Database Connection Issues**: Verify `DATABASE_URL` is set correctly
- **Static Files Not Loading**: Ensure static folder paths are correct

## Support

For Render-specific issues, check:
- Render Documentation: https://render.com/docs
- Render Community: https://community.render.com

