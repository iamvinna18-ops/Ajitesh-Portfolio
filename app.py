import os
from datetime import datetime, timezone

from flask import Flask, flash, redirect, render_template, request, session, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func
from sqlalchemy.engine import make_url

app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "change-this-local-development-key")

database_url = os.environ.get("DATABASE_URL", "sqlite:///portfolio.db")
if database_url.startswith("postgres://"):
    database_url = database_url.replace("postgres://", "postgresql://", 1)
# Neon and most hosted PostgreSQL providers support psycopg 3.
if database_url.startswith("postgresql://") and "+psycopg" not in database_url:
    database_url = database_url.replace("postgresql://", "postgresql+psycopg://", 1)

app.config["SQLALCHEMY_DATABASE_URI"] = database_url
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {"pool_pre_ping": True}
db = SQLAlchemy(app)


class ContactMessage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(254), nullable=False)
    subject = db.Column(db.String(150), nullable=False)
    message = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)


class Visit(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    visited_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)


with app.app_context():
    db.create_all()


@app.context_processor
def inject_globals():
    total_visits = db.session.query(func.count(Visit.id)).scalar() or 0
    return {"total_visits": total_visits, "current_year": datetime.now().year}


@app.route("/")
def home():
    if not session.get("counted_visit"):
        db.session.add(Visit())
        db.session.commit()
        session["counted_visit"] = True
    return render_template("index.html", page="home")


@app.route("/contact", methods=["POST"])
def contact():
    # A hidden honeypot field helps filter basic automated spam.
    if request.form.get("website"):
        flash("Thanks! Your message has been received.", "success")
        return redirect(url_for("home") + "#contact")

    name = request.form.get("name", "").strip()
    email = request.form.get("email", "").strip()
    subject = request.form.get("subject", "").strip()
    message = request.form.get("message", "").strip()

    if not all([name, email, subject, message]):
        flash("Please complete every field.", "error")
    elif len(name) > 100 or len(email) > 254 or len(subject) > 150 or len(message) > 5000:
        flash("One or more fields are too long. Please shorten your message.", "error")
    elif "@" not in email or "." not in email.rsplit("@", 1)[-1]:
        flash("Please enter a valid email address.", "error")
    else:
        db.session.add(ContactMessage(name=name, email=email, subject=subject, message=message))
        db.session.commit()
        flash("Message sent successfully. Thank you for reaching out!", "success")

    return redirect(url_for("home") + "#contact")


@app.route("/health")
def health():
    return {"status": "ok"}


if __name__ == "__main__":
    app.run(debug=True)
