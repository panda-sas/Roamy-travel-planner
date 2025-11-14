# Streamlit Cloud Deployment Guide for Roamy

## Quick Setup Steps

### 1. Go to Streamlit Cloud
Visit: **https://share.streamlit.io**

### 2. Sign In
- Click "Sign in" 
- Choose "Continue with GitHub"
- Authorize Streamlit Cloud to access your GitHub account

### 3. Create New App
- Click the **"New app"** button (top right)
- Or go to: https://share.streamlit.io/deploy

### 4. Configure Your App

**Repository:** `panda-sas/Roamy-travel-planner`  
**Branch:** `main`  
**Main file path:** `app.py`  
**App URL:** (auto-generated, e.g., `roamy-travel-planner.streamlit.app`)

### 5. Add Secrets (IMPORTANT!)

Click **"Advanced settings"** → **"Secrets"** and add:

```toml
OPENAI_API_KEY = "sk-your-openai-api-key-here"
```

**How to get your OpenAI API key:**
1. Go to https://platform.openai.com/api-keys
2. Sign in or create an account
3. Click "Create new secret key"
4. Copy the key (you won't see it again!)
5. Paste it in Streamlit Cloud secrets

### 6. Deploy!

Click **"Deploy"** and wait 1-2 minutes for the app to build and deploy.

## Your App Will Be Live At:
`https://roamy-travel-planner.streamlit.app`  
(or similar URL based on your app name)

## Troubleshooting

### App won't start
- ✅ Check that `OPENAI_API_KEY` is set in Secrets
- ✅ Verify the API key is valid (starts with `sk-`)
- ✅ Check the logs in Streamlit Cloud dashboard

### Import errors
- ✅ Make sure `requirements.txt` is in the root directory
- ✅ Check that all dependencies are listed correctly

### API errors
- ✅ Verify your OpenAI API key has credits/usage available
- ✅ Check OpenAI dashboard for rate limits

### App is slow
- ✅ This is normal - the agent makes multiple LLM calls
- ✅ Consider upgrading to a faster OpenAI model in `agents/trip_planner.py`

## Updating Your App

After pushing changes to GitHub:
1. Go to your app in Streamlit Cloud dashboard
2. Click **"⋮"** (three dots) → **"Reboot app"**
3. Or it will auto-update (may take a few minutes)

## Custom Domain (Optional)

1. Go to app settings
2. Click "Custom domain"
3. Follow instructions to add your domain

## Monitoring

- View logs: Dashboard → Your App → "Logs"
- View metrics: Dashboard → Your App → "Metrics"
- Check usage: Dashboard → Your App → "Usage"

## Cost Considerations

- **Streamlit Cloud**: Free tier available
- **OpenAI API**: Pay per use (check pricing at platform.openai.com)
- Monitor usage in OpenAI dashboard to avoid surprises

## Security Notes

- ✅ Never commit `.env` file (already in `.gitignore`)
- ✅ Use Streamlit Cloud Secrets for API keys
- ✅ Your API key is encrypted in Streamlit Cloud
- ✅ Consider setting usage limits in OpenAI dashboard

## Next Steps After Deployment

1. ✅ Test all features in production
2. ✅ Share your app URL with users
3. ✅ Monitor API usage and costs
4. ✅ Set up alerts if needed
5. ✅ Consider adding analytics (optional)

---

**Need Help?** Check the main [DEPLOYMENT.md](DEPLOYMENT.md) file for more details.

