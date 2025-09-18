# Render Deployment Guide

This guide will help you deploy your Django backend to Render's free plan.

## Prerequisites

1. A GitHub account with your code pushed to a repository
2. A Render account (sign up at render.com)
3. Your Capacitor.js frontend (CORS is configured to allow all origins)

## Step 1: Prepare Your Repository

Your project is already configured with the necessary files:
- ✅ `render.yaml` - Render configuration
- ✅ `requirements.txt` - Python dependencies
- ✅ `Procfile` - Process configuration
- ✅ Updated `settings.py` - Environment variable support

## Step 2: Deploy to Render

### Option A: Using render.yaml (Recommended)

1. **Push your code to GitHub** (if not already done):
   ```bash
   git add .
   git commit -m "Prepare for Render deployment"
   git push origin main
   ```

2. **Connect to Render**:
   - Go to [render.com](https://render.com) and sign in
   - Click "New +" → "Blueprint"
   - Connect your GitHub repository
   - Select your repository and branch

3. **Render will automatically detect the `render.yaml` file** and use those settings.

### Option B: Manual Configuration

If you prefer manual setup:

1. **Create a new Web Service**:
   - Go to Render Dashboard
   - Click "New +" → "Web Service"
   - Connect your GitHub repository

2. **Configure the service**:
   - **Name**: `route-monitor-backend`
   - **Environment**: `Python 3`
   - **Region**: Choose closest to your users
   - **Branch**: `main`
   - **Root Directory**: Leave empty
   - **Build Command**: 
     ```bash
     pip install -r requirements.txt && python manage.py collectstatic --noinput && python manage.py migrate
     ```
   - **Start Command**: 
     ```bash
     gunicorn route_monitor.wsgi:application
     ```

## Step 3: Set Up Database

### PostgreSQL (Free Plan) - **Recommended**
- PostgreSQL database is automatically created by `render.yaml`
- Database URL is automatically configured
- Better performance and features than SQLite
- Data migration script included

## Step 4: Configure Environment Variables

Environment variables are automatically configured by `render.yaml`:
- ✅ `DEBUG=false`
- ✅ `DJANGO_SECRET_KEY` (auto-generated)
- ✅ `ALLOWED_HOSTS` (your Render domain)
- ✅ `DATABASE_URL` (PostgreSQL connection string)

### CORS Configuration:
```
# CORS is already configured to allow all origins for Capacitor.js
# No additional configuration needed
```

## Step 5: Migrate Your Data

After your Render deployment is live, migrate your data:

1. **SSH into your Render service** (or use Render's web console)
2. **Upload the fixtures.json file** to your service
3. **Run the migration script**:
   ```bash
   python migrate_to_render_postgres.py
   ```

This will import all your data from Railway to the new Render PostgreSQL database.

## Step 6: Update Your Frontend

After deployment, update your frontend to use the new Render URL:
- Your backend will be available at: `https://your-app-name.onrender.com`
- Update API calls in your frontend to point to this new URL

## Step 7: Test Your Deployment

1. **Check the service logs** in Render dashboard
2. **Test your API endpoints**:
   ```bash
   curl https://your-app-name.onrender.com/api/your-endpoint/
   ```
3. **Verify CORS is working** from your frontend

## Free Plan Limitations

- **Sleep after 15 minutes** of inactivity
- **750 hours/month** of uptime
- **512MB RAM**
- **1GB disk space**
- **No custom domains** (use .onrender.com subdomain)

## Troubleshooting

### Common Issues:

1. **Build fails**:
   - Check the build logs in Render dashboard
   - Ensure all dependencies are in `requirements.txt`

2. **Static files not loading**:
   - Verify `STATIC_ROOT` and `STATICFILES_STORAGE` settings
   - Check that `collectstatic` runs during build

3. **Database errors**:
   - Ensure migrations run during build
   - Check database URL format

4. **CORS errors**:
   - Update `CORS_ORIGINS` environment variable
   - Include your frontend domain

### Getting Help:
- Check Render's documentation: https://render.com/docs
- View service logs in Render dashboard
- Check Django logs for detailed error messages

## Migration from Railway

1. **Export data from Railway** (if needed):
   - Use Django's `dumpdata` command
   - Or export directly from Railway's database

2. **Import data to Render**:
   - Use Django's `loaddata` command
   - Or import through Django admin

3. **Update DNS/domains**:
   - Update any hardcoded URLs
   - Update frontend configuration

## Cost Comparison

- **Railway**: $20/month
- **Render Free**: $0/month (with limitations)
- **Render Starter**: $7/month (if you need more resources)

You'll save $20/month by switching to Render's free plan!
