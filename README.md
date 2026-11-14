# Ajitesh — Developer Portfolio

A standalone, responsive Flask portfolio with an animated dark interface, contact form, visitor counter and SQL database.

## Run locally

1. Install Python 3.10 or newer.
2. Open a terminal in this folder.
3. Create and activate a virtual environment:

   **Windows**
   ```bash
   py -m venv .venv
   .venv\\Scripts\\activate
   ```

   **macOS/Linux**
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

4. Install packages:
   ```bash
   pip install -r requirements.txt
   ```
5. Start:
   ```bash
   python app.py
   ```
6. Visit http://127.0.0.1:5000

By default the app uses local SQLite (`portfolio.db`).

## Persistent free database for deployment

Render free web services have an ephemeral filesystem, so do not use the local SQLite file for production data. Create a free PostgreSQL project at Neon, copy its connection string, and set it as the `DATABASE_URL` environment variable in Render. The app uses PostgreSQL when `DATABASE_URL` is set and SQLite locally.

Neon free-plan limits can change; check its current pricing page before relying on the allowance. Keep database credentials private and never commit them to GitHub.

## Deploy to Render

1. Push this folder to a GitHub repository.
2. In Render, choose **New → Web Service** and connect the repository.
3. Select **Free**.
4. Build command: `pip install -r requirements.txt`
5. Start command: `gunicorn app:app`
6. Add environment variables:
   - `SECRET_KEY`: a long random secret
   - `DATABASE_URL`: Neon PostgreSQL connection string
7. Deploy. Render provides an `onrender.com` URL.

The free Render web service sleeps after inactivity and may take about a minute to wake up. Free plans and limits can change.

## Personalize before publishing

Edit `templates/index.html` and replace the sample email, GitHub, LinkedIn, education details and project descriptions with your real information. The current content is a starter draft; verify every detail before publishing.
