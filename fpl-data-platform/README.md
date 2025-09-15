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

## Hosting on Heroku

 We will be using Heroku to deploy the Flask application. Heroku is one of many cloud platforms as a service (PaaS). Once the application is deployed, we will get a public URL that makes our application accessible by any device connected to the internet.  Follow the steps below to host your Flask application on Heroku:

1. To get things started, install Gunicorn: pip install gunicorn
2. We need to add two additional files to the remote repository.  The first file would be a text file that list the modules our application depends on. To do so execute: pip freeze > requirements.txt
3. Next we need to create a Procfile at the root of the directory. A Procfile tells Heroku how to run our application. We create the Procfile using: echo "web: gunicorn src.app:app" > Procfile
4. Once you have created the two aforementioned files, push them to your remote repository.
5. If you do not have an account with Heroku, you need to [create an account](https://signup.heroku.com/). 
6. Once you have logged in and accessed the dashboard, click on the "New" button located on the top right corner of the screen. Afterwards, select "Create new app".
7. After creating the app, you should be redirected to a screen resembling the image below. The next step entails connecting your GitHub repository to the Heroku application. Click on the "GitHub Connect to GitHub" button.

