# Deployment Guide for Event Planner Agent

## Overview

Deploy the Event Planner Agent to free hosting platforms. The app is lightweight and suitable for serverless or containerized deployments.

## Prerequisites

- Git repository with your code
- API keys configured in environment variables
- Python 3.10+ runtime

## Free Hosting Options

### 1. Railway

Railway offers free tier with 512MB RAM, 1GB disk, and PostgreSQL.

**Steps:**
1. Sign up at [Railway.app](https://railway.app)
2. Connect your GitHub repo
3. Set environment variables in Railway dashboard:
   - `EVENTBRITE_API_KEY`
   - `GOOGLE_SHEETS_CREDENTIALS_FILE` (upload JSON content as env var)
   - `GOOGLE_SHEETS_SPREADSHEET_ID`
   - `SMTP_SERVER`, `SMTP_PORT`, `SMTP_USERNAME`, `SMTP_PASSWORD`
   - `SECRET_KEY` (generate random string)
   - `LOG_LEVEL=INFO`
4. Deploy automatically on push

**Railway Commands:**
```bash
# Install Python buildpack
railway add --name event-planner

# Set Python version
echo "python-3.10" > runtime.txt

# Deploy
railway up
```

### 2. Render

Render provides free web services with 750 hours/month.

**Steps:**
1. Sign up at [Render.com](https://render.com)
2. Create new Web Service from Git
3. Select your repo
4. Configure:
   - Runtime: Python 3
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `python -m app.main`
5. Add environment variables in Render dashboard
6. Deploy

### 3. Vercel

For serverless deployment (requires Flask adaptation).

**Steps:**
1. Install Vercel CLI: `npm i -g vercel`
2. Create `vercel.json`:
   ```json
   {
     "version": 2,
     "builds": [
       {
         "src": "app/main.py",
         "use": "@vercel/python"
       }
     ],
     "routes": [
       {
         "src": "/(.*)",
         "dest": "app/main.py"
       }
     ]
   }
   ```
3. Deploy: `vercel --prod`
4. Set environment variables in Vercel dashboard

## Environment Variables

Required for all deployments:

```
EVENTBRITE_API_KEY=your_eventbrite_key
GOOGLE_SHEETS_CREDENTIALS_FILE={"type":"service_account","project_id":...}
GOOGLE_SHEETS_SPREADSHEET_ID=your_sheet_id
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=your_email@gmail.com
SMTP_PASSWORD=your_app_password
SECRET_KEY=your_random_secret_key
LOG_LEVEL=INFO
```

## Post-Deployment Checklist

- [ ] App loads at deployed URL
- [ ] Event creation works
- [ ] Venue suggestions load (with fallback if API fails)
- [ ] RSVP management functions
- [ ] To-do generation works
- [ ] Export functionality works
- [ ] Logs are accessible

## Troubleshooting

- **Build Failures**: Check Python version compatibility
- **API Errors**: Verify environment variables are set correctly
- **Timeout Issues**: Increase timeout limits in hosting platform settings
- **Database Issues**: Ensure CSV files have write permissions

## Scaling

For higher usage:
- Upgrade to paid plans on Railway/Render
- Migrate to Heroku or AWS for more resources
- Consider database migration from CSV to PostgreSQL/MySQL

## Monitoring

- Check application logs in hosting dashboard
- Monitor API usage on Eventbrite/Google Cloud
- Set up uptime monitoring (e.g., UptimeRobot free tier)
