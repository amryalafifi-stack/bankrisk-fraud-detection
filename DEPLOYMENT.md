# BankRisk Deployment Guide

## Quick Start (Local)

```bash
# Install dependencies
pip3 install -r requirements.txt

# Run the application
streamlit run app.py
```

Access at: `http://localhost:8501`

---

## Deployment Options

### 1. Streamlit Community Cloud (Easiest)

**Steps:**
1. Push code to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Click "New app" → Select your repo → Choose `app.py`
4. Deploy!

**Note:** The 150MB `fraudTest.csv` may exceed GitHub's file size limit. Either:
- Use Git LFS for large files
- Remove it and rely on synthetic data generation
- Host dataset separately (S3, Google Drive) and load via URL

---

### 2. Heroku

**Setup:**
```bash
# Create Procfile
echo "web: streamlit run app.py --server.port=\$PORT --server.headless=true" > Procfile

# Deploy
heroku create your-app-name
git push heroku main
```

**Cost:** ~$7/month (Hobby dyno)

---

### 3. Docker (AWS/GCP/Azure)

**Dockerfile:**
```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8501
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.headless=true"]
```

**Build & Run:**
```bash
docker build -t bankrisk .
docker run -p 8501:8501 bankrisk
```

---

## Production Checklist

- [ ] Add user authentication (Streamlit-Authenticator)
- [ ] Integrate payment system (Stripe/Whop)
- [ ] Set up database for user management (PostgreSQL)
- [ ] Configure environment variables for secrets
- [ ] Enable HTTPS/SSL
- [ ] Set up monitoring (Sentry, DataDog)
- [ ] Implement rate limiting
- [ ] Add data export features (PDF/CSV)

---

## Environment Variables

Create `.streamlit/secrets.toml` for production:

```toml
[general]
SALT = "your-secure-salt-here"
FREE_SEARCH_LIMIT = 1

[stripe]
api_key = "sk_live_..."
webhook_secret = "whsec_..."
```

---

## Support

For issues or questions, contact: [your-email@example.com]
