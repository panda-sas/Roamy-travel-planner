# Deployment Guide for Roamy

This guide covers multiple deployment options for Roamy - AI Travel Planner.

## Prerequisites

- OpenAI API key
- Git repository (for most platforms)
- Account on your chosen deployment platform

## Option 1: Streamlit Cloud (Recommended - Easiest)

Streamlit Cloud is the simplest way to deploy Streamlit apps.

### Steps:

1. **Push your code to GitHub**
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git remote add origin <your-github-repo-url>
   git push -u origin main
   ```

2. **Deploy on Streamlit Cloud**
   - Go to [share.streamlit.io](https://share.streamlit.io)
   - Sign in with GitHub
   - Click "New app"
   - Select your repository and branch
   - Set main file path: `app.py`
   - Click "Deploy"

3. **Add Environment Variables**
   - In Streamlit Cloud dashboard, go to "Settings" → "Secrets"
   - Add your OpenAI API key:
     ```toml
     OPENAI_API_KEY = "your-api-key-here"
     ```

4. **Access your app**
   - Your app will be available at `https://your-app-name.streamlit.app`

### Advantages:
- ✅ Free tier available
- ✅ Automatic HTTPS
- ✅ Easy updates (just push to GitHub)
- ✅ Built-in secrets management

---

## Option 2: Docker Deployment

Deploy using Docker on any platform that supports containers.

### Build and Run Locally:

```bash
# Build the image
docker build -t roamy .

# Run the container
docker run -p 8501:8501 -e OPENAI_API_KEY=your-key-here roamy
```

### Using Docker Compose:

```bash
# Make sure .env file exists with OPENAI_API_KEY
docker-compose up -d
```

### Deploy to Cloud Platforms:

#### Railway
1. Install Railway CLI: `npm i -g @railway/cli`
2. Run: `railway login` and `railway init`
3. Add `OPENAI_API_KEY` in Railway dashboard
4. Deploy: `railway up`

#### Render
1. Create new Web Service
2. Connect your GitHub repo
3. Set:
   - Build Command: `docker build -t roamy .`
   - Start Command: `docker run -p $PORT:8501 -e OPENAI_API_KEY=$OPENAI_API_KEY roamy`
4. Add `OPENAI_API_KEY` in Environment variables

#### Fly.io
```bash
# Install flyctl
curl -L https://fly.io/install.sh | sh

# Launch app
fly launch

# Set secrets
fly secrets set OPENAI_API_KEY=your-key-here
```

---

## Option 3: Heroku

### Steps:

1. **Install Heroku CLI**
   ```bash
   # macOS
   brew tap heroku/brew && brew install heroku
   ```

2. **Login and Create App**
   ```bash
   heroku login
   heroku create roamy-app
   ```

3. **Set Environment Variables**
   ```bash
   heroku config:set OPENAI_API_KEY=your-api-key-here
   ```

4. **Deploy**
   ```bash
   git push heroku main
   ```

5. **Open App**
   ```bash
   heroku open
   ```

---

## Option 4: AWS/Azure/GCP

### AWS (EC2 + Docker)

1. Launch EC2 instance (Ubuntu)
2. Install Docker:
   ```bash
   sudo apt update
   sudo apt install docker.io docker-compose -y
   ```
3. Clone repo and deploy:
   ```bash
   git clone <your-repo>
   cd travel-planner
   docker-compose up -d
   ```

### Azure Container Instances

```bash
# Build and push to Azure Container Registry
az acr build --registry <registry-name> --image roamy:latest .

# Create container instance
az container create \
  --resource-group <resource-group> \
  --name roamy \
  --image <registry-name>.azurecr.io/roamy:latest \
  --dns-name-label roamy \
  --ports 8501 \
  --environment-variables OPENAI_API_KEY=your-key
```

### Google Cloud Run

```bash
# Build and deploy
gcloud builds submit --tag gcr.io/<project-id>/roamy
gcloud run deploy roamy \
  --image gcr.io/<project-id>/roamy \
  --platform managed \
  --region us-central1 \
  --set-env-vars OPENAI_API_KEY=your-key \
  --allow-unauthenticated
```

---

## Option 5: VPS Deployment (DigitalOcean, Linode, etc.)

1. **SSH into your VPS**
   ```bash
   ssh user@your-server-ip
   ```

2. **Install Dependencies**
   ```bash
   sudo apt update
   sudo apt install python3-pip python3-venv nginx -y
   ```

3. **Clone and Setup**
   ```bash
   git clone <your-repo-url>
   cd travel-planner
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

4. **Create Systemd Service**
   ```bash
   sudo nano /etc/systemd/system/roamy.service
   ```
   
   Add:
   ```ini
   [Unit]
   Description=Roamy Travel Planner
   After=network.target

   [Service]
   Type=simple
   User=your-user
   WorkingDirectory=/home/your-user/travel-planner
   Environment="PATH=/home/your-user/travel-planner/venv/bin"
   Environment="OPENAI_API_KEY=your-key-here"
   ExecStart=/home/your-user/travel-planner/venv/bin/streamlit run app.py --server.port=8501
   Restart=always

   [Install]
   WantedBy=multi-user.target
   ```

5. **Start Service**
   ```bash
   sudo systemctl daemon-reload
   sudo systemctl enable roamy
   sudo systemctl start roamy
   ```

6. **Setup Nginx Reverse Proxy**
   ```bash
   sudo nano /etc/nginx/sites-available/roamy
   ```
   
   Add:
   ```nginx
   server {
       listen 80;
       server_name your-domain.com;

       location / {
           proxy_pass http://127.0.0.1:8501;
           proxy_http_version 1.1;
           proxy_set_header Upgrade $http_upgrade;
           proxy_set_header Connection "upgrade";
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
           proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
           proxy_set_header X-Forwarded-Proto $scheme;
       }
   }
   ```

7. **Enable and Restart Nginx**
   ```bash
   sudo ln -s /etc/nginx/sites-available/roamy /etc/nginx/sites-enabled/
   sudo nginx -t
   sudo systemctl restart nginx
   ```

---

## Environment Variables

All deployment methods require the `OPENAI_API_KEY` environment variable:

- **Streamlit Cloud**: Add in Secrets tab
- **Docker**: Use `-e OPENAI_API_KEY=...` or `.env` file
- **Heroku**: Use `heroku config:set`
- **AWS/Azure/GCP**: Add in platform's environment variables section

---

## Security Considerations

1. **Never commit `.env` file** - Already in `.gitignore`
2. **Use platform secrets management** for API keys
3. **Enable HTTPS** - Most platforms provide this automatically
4. **Set up rate limiting** if expecting high traffic
5. **Monitor API usage** to avoid unexpected costs

---

## Monitoring and Maintenance

### Health Checks
The Dockerfile includes a health check. Monitor:
- Application logs
- API usage and costs
- Response times

### Updates
- **Streamlit Cloud**: Auto-deploys on git push
- **Docker**: Rebuild and redeploy
- **VPS**: Pull latest code and restart service

---

## Cost Estimates

- **Streamlit Cloud**: Free tier available
- **Railway/Render**: ~$5-20/month
- **Heroku**: Free tier (limited), then ~$7/month
- **AWS/Azure/GCP**: Pay-as-you-go, ~$10-50/month
- **VPS**: $5-20/month depending on provider

---

## Troubleshooting

**Issue**: App won't start
- Check environment variables are set
- Verify OpenAI API key is valid
- Check logs: `docker logs <container>` or `journalctl -u roamy`

**Issue**: Slow responses
- Consider upgrading to faster LLM model
- Add caching for common queries
- Scale up resources

**Issue**: API rate limits
- Implement request queuing
- Add retry logic with exponential backoff
- Consider upgrading OpenAI plan

---

## Next Steps

After deployment:
1. Test all features in production
2. Set up monitoring/alerting
3. Configure custom domain (if needed)
4. Set up CI/CD for automated deployments
5. Add analytics (optional)

