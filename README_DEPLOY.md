# Deployment Guide

This file explains several simple ways to deploy the `Aadhaar Insight AI` Streamlit app.

## Option A — Streamlit Community Cloud (recommended for quick sharing)

1. Create a GitHub repo and push this project (do NOT include `unified_enrolment_data.csv`).
2. Sign in to Streamlit Cloud (https://streamlit.io/cloud) and connect your GitHub account.
3. Create a new app, point it at the repo and branch, and set the main file to `app1.py`.
4. Add environment variables or secrets in the Streamlit Cloud settings if needed.

Notes:
- Streamlit Cloud automatically reads `requirements.txt`.
- Use a small sample dataset for public sharing.

## Option B — Docker (portable, reproducible)

Create a `Dockerfile` in the project root:

```dockerfile
FROM python:3.10-slim
WORKDIR /app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY . /app
EXPOSE 8501
CMD ["streamlit", "run", "app1.py", "--server.port", "8501", "--server.headless", "true"]
```

Build and run locally:

```bash
docker build -t aadhaar-dashboard:latest .
docker run -p 8501:8501 aadhaar-dashboard:latest
```

## Option C — Deploy on Azure Web App for Containers

1. Build Docker image (see Docker section).
2. Push to Azure Container Registry.
3. Create a Web App (Linux) and configure to pull container from ACR.
4. Set `WEBSITES_PORT=8501` application setting.

## Option D — VPS (Ubuntu) — simple manual deployment

```bash
# On server
sudo apt update && sudo apt install python3 python3-venv git -y
git clone <your-repo>
cd enrollment_dashboard
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
# run with tmux or systemd
streamlit run app1.py --server.port 8501
```

## Option E — Heroku (if preferred)

Heroku may require extra buildpack adjustments — not the recommended path for Streamlit.
A Docker deployment is simpler for Heroku if needed.

## Handling Data on Deployment

- Do NOT commit `unified_enrolment_data.csv` to public repos.
- Use Streamlit secrets or environment variables to provide remote data paths or API credentials.
- For large datasets, store CSV in cloud storage (S3/GCS) and download in app startup.

## Monitoring & Logs

- Streamlit Cloud provides logs in its dashboard.
- For Docker/VPS — configure systemd service and forward logs to a file or use `journalctl`.

## Security

- Keep sensitive files out of the repo (add to `.gitignore`).
- Restrict access to deployed endpoints if data is private.

---

If you want, I can also add a `Dockerfile` and a simple `systemd` service template into the repo.