# FPL Data Analysis Platform

This is a simple Flask web app that fetches data from the Fantasy Premier League API and displays:
- Player list (/api/players)
- Team info (/api/teams)
- Match fixtures (/api/fixtures)

It also includes a basic form input on the homepage to echo user input for assignment requirement.

## Run Locally

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
export FLASK_APP=src/app.py
flask run
```

## Deploy to Heroku

Make sure you have `requirements.txt` and `Procfile`, then:

```bash
git init
heroku create
git add .
git commit -m "Initial commit"
git push heroku main
```
