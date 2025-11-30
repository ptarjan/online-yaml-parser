# Deployment Instructions for Google Cloud

This application has been migrated from Python 2.7 to Python 3.12 for deployment on Google App Engine.

## Prerequisites

1. **Google Cloud Account**: You need a Google Cloud account with billing enabled
2. **Google Cloud SDK**: Install the gcloud CLI tool
   - Download from: https://cloud.google.com/sdk/docs/install
   - Or use Cloud Shell in the Google Cloud Console

3. **Google Cloud Project**: Create or select a project
   ```bash
   gcloud projects create [PROJECT_ID]
   # or
   gcloud config set project [PROJECT_ID]
   ```

## Deployment Steps

1. **Authenticate with Google Cloud**
   ```bash
   gcloud auth login
   ```

2. **Set your project** (if not already set)
   ```bash
   gcloud config set project [YOUR_PROJECT_ID]
   ```

3. **Enable required APIs**
   ```bash
   gcloud services enable appengine.googleapis.com
   ```

4. **Initialize App Engine** (first time only)
   ```bash
   gcloud app create --region=[REGION]
   ```
   Choose a region close to your users (e.g., `us-central`, `europe-west`, `asia-northeast1`)

5. **Deploy the application**
   ```bash
   gcloud app deploy
   ```

   When prompted, confirm the deployment by typing `Y`

6. **View your application**
   ```bash
   gcloud app browse
   ```
   Or visit: `https://[YOUR_PROJECT_ID].appspot.com`

## Viewing Logs

To view application logs:
```bash
gcloud app logs tail -s default
```

## Configuration

The application is configured in `app.yaml`:
- Runtime: Python 3.12
- Max instances: 1 (to keep costs low)
- Static files: `/js` directory and `ads.txt`

## Costs

Google App Engine offers a free tier with:
- 28 instance hours per day
- 1 GB of egress per day
- 5 GB Cloud Storage

With `max_instances: 1`, the app should stay within the free tier for low to moderate traffic.

## Updating the Application

To deploy updates:
1. Make your code changes
2. Run `gcloud app deploy` again
3. Confirm the deployment

## Rolling Back

To rollback to a previous version:
```bash
gcloud app versions list
gcloud app versions migrate [VERSION_ID]
```

## Custom Domain

To use a custom domain:
1. Go to App Engine > Settings > Custom domains in the Cloud Console
2. Follow the wizard to add and verify your domain
3. Update your DNS records as instructed

## Support

- Google Cloud Documentation: https://cloud.google.com/appengine/docs/standard/python3
- Pricing: https://cloud.google.com/appengine/pricing
