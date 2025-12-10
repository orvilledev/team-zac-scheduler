# Render Deployment Checklist

Use this checklist to ensure a smooth deployment to Render.

## Pre-Deployment Checklist

### ✅ Code Preparation
- [x] All code committed to Git
- [x] `render.yaml` created
- [x] `Procfile` created
- [x] `requirements.txt` includes all dependencies
- [x] `gunicorn_config.py` configured for Render
- [x] `config.py` handles PostgreSQL URLs
- [x] Database initialization script ready (`init_render_db.py`)
- [x] `.gitignore` excludes sensitive files

### ✅ Files to Verify
- [ ] `render.yaml` - Render blueprint configuration
- [ ] `Procfile` - Process definition
- [ ] `build.sh` - Build script (optional)
- [ ] `gunicorn_config.py` - Gunicorn configuration
- [ ] `config.py` - Updated for PostgreSQL
- [ ] `requirements.txt` - Includes `psycopg2-binary`
- [ ] `init_render_db.py` - Database initialization script
- [ ] `create_admin.py` - Admin user creation script

## Deployment Steps

### Step 1: Push to GitHub
```bash
git add .
git commit -m "Prepare for Render deployment"
git push origin main
```

### Step 2: Create Render Account
- [ ] Sign up at https://render.com (if not already)
- [ ] Verify email address

### Step 3: Deploy via Blueprint (Recommended)
- [ ] Go to Render Dashboard
- [ ] Click "New" → "Blueprint"
- [ ] Connect your GitHub account
- [ ] Select your repository
- [ ] Render will auto-detect `render.yaml`
- [ ] Review the services (Web Service + PostgreSQL)
- [ ] Click "Apply"

### Step 4: Configure Environment Variables
After deployment starts, set these in your Web Service settings:

**Required:**
- [ ] `SECRET_KEY` - Generate a strong key (Render can auto-generate)

**Optional (if using Redis/Celery):**
- [ ] `REDIS_URL` - Redis connection string
- [ ] `CELERY_BROKER_URL` - Celery broker URL
- [ ] `CELERY_RESULT_BACKEND` - Celery result backend

**Note:** `DATABASE_URL` is automatically set by Render when you link the PostgreSQL database.

### Step 5: Wait for Deployment
- [ ] Monitor build logs
- [ ] Wait for "Live" status
- [ ] Note your app URL (e.g., `https://your-app.onrender.com`)

### Step 6: Initialize Database
- [ ] Open Render Shell (in your web service dashboard)
- [ ] Run: `python init_render_db.py`
- [ ] Verify output shows successful initialization
- [ ] Default admin user created (username: `admin`)

### Step 7: Test Your Application
- [ ] Visit your app URL
- [ ] Test login with username: `admin` (no password)
- [ ] Verify all features work
- [ ] Check file uploads work
- [ ] Test database operations

## Post-Deployment Tasks

### Create Additional Users
- [ ] Use Render Shell: `python create_admin.py`
- [ ] Or create users through the web interface

### Configure Custom Domain (Optional)
- [ ] Go to Web Service → Settings → Custom Domains
- [ ] Add your domain
- [ ] Update DNS records as instructed

### Set Up Backups
- [ ] Configure PostgreSQL backups in Render dashboard
- [ ] Set backup schedule (recommended: daily)

### Monitor Performance
- [ ] Check Render dashboard for metrics
- [ ] Monitor logs for errors
- [ ] Set up alerts if needed

## Troubleshooting

### Build Fails
- Check build logs in Render dashboard
- Verify all dependencies in `requirements.txt`
- Ensure Python version is compatible

### App Crashes
- Check runtime logs
- Verify environment variables are set
- Check database connection

### Database Issues
- Verify `DATABASE_URL` is set correctly
- Run `init_render_db.py` again if needed
- Check PostgreSQL service is running

### Static Files Not Loading
- Verify static folder paths in `config.py`
- Check file permissions
- Ensure files are committed to Git

## Important Notes

⚠️ **Free Tier Limitations:**
- App spins down after 15 minutes of inactivity
- First request after spin-down takes 30-60 seconds
- Consider upgrading for production use

⚠️ **File Storage:**
- Uploaded files stored in filesystem
- Files may be lost during redeployments on free tier
- Consider cloud storage (S3, Cloudinary) for production

⚠️ **Database:**
- PostgreSQL database is persistent
- Free tier has 90-day data retention
- Backup regularly

## Support Resources

- Render Documentation: https://render.com/docs
- Render Community: https://community.render.com
- Render Status: https://status.render.com

---

**Ready to deploy?** Follow the steps above and check off each item as you complete it!

