from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta
import requests

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///players.db'
db = SQLAlchemy(app)
FPL_BASE = "https://fantasy.premierleague.com/api"

class Player(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    team = db.Column(db.String(30))
    total_points = db.Column(db.Integer)
    price = db.Column(db.Float)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

def get_team_mapping():
    try:
        response = requests.get(f"{FPL_BASE}/bootstrap-static/")
        if response.status_code == 200:
            teams = response.json().get("teams", [])
            return {t["id"]: t["name"] for t in teams}
    except:
        return {}
    return {}

@app.route("/", methods=["GET"])
def index():
    return '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>FPL Data Analysis Platform</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                background: linear-gradient(to right, #4b79a1, #283e51);
                color: white;
                text-align: center;
                padding: 80px;
            }
            input[type="text"] {
                padding: 10px;
                width: 300px;
                border-radius: 6px;
                border: none;
            }
            input[type="submit"] {
                padding: 10px 20px;
                border-radius: 6px;
                border: none;
                background-color: #1abc9c;
                color: white;
                cursor: pointer;
            }
            .links {
                margin-top: 40px;
            }
            .links a {
                color: #ecf0f1;
                margin: 0 10px;
            }
        </style>
    </head>
    <body>
        <h1>⚽ FPL Data Analysis Platform</h1>
        <p>Enter your favorite Fantasy Premier League player below:</p>
        <form action="/echo_user_input" method="POST">
            <input type="text" name="user_input" placeholder="e.g., Erling Haaland" required>
            <input type="submit" value="Submit">
        </form>

        <div class="links">
            <h3>📊 Data Endpoints</h3>
            <a href="/api/players" target="_blank">Players</a>
            <a href="/api/teams" target="_blank">Teams</a>
            <a href="/api/fixtures" target="_blank">Fixtures</a>
        </div>
    </body>
    </html>
    '''

@app.route("/echo_user_input", methods=["POST"])
def echo():
    user_input = request.form.get("user_input", "No input")
    return f"<h3>You entered: <b>{user_input}</b></h3>"

@app.route("/api/players", methods=["GET"])
def get_players():
    response = requests.get(f"{FPL_BASE}/bootstrap-static/")
    if response.status_code != 200:
        return jsonify({"error": "Failed to fetch player data"}), 500

    data = response.json()
    players = data.get("elements", [])
    teams = {team["id"]: team["name"] for team in data.get("teams", [])}

    # 取总得分前10名球员
    top_players = sorted(players, key=lambda p: p["total_points"], reverse=True)[:10]

    # 构建 HTML 表格行
    rows = ""
    for p in top_players:
        name = f"{p['first_name']} {p['second_name']}"
        team_name = teams.get(p["team"], f"Team {p['team']}")
        position = {1: "GK", 2: "DEF", 3: "MID", 4: "FWD"}.get(p["element_type"], "Unknown")
        total_points = p["total_points"]
        price = p["now_cost"] / 10  # 原始单位是 10x

        rows += f"""
        <tr>
            <td>{name}</td>
            <td>{team_name}</td>
            <td>{position}</td>
            <td>{total_points}</td>
            <td>£{price:.1f}m</td>
        </tr>
        """

    return f'''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Top 10 FPL Players</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
                background: linear-gradient(to right, #4b79a1, #283e51);
                color: white;
                text-align: center;
                padding: 50px;
            }}
            table {{
                margin: auto;
                width: 80%;
                border-collapse: collapse;
                background-color: rgba(255, 255, 255, 0.1);
                border-radius: 8px;
                overflow: hidden;
            }}
            th, td {{
                padding: 12px;
                border-bottom: 1px solid #ddd;
                color: white;
            }}
            th {{
                background-color: #1abc9c;
            }}
        </style>
    </head>
    <body>
        <h1>🌟 Top 10 FPL Players</h1>
        <table>
            <tr>
                <th>Name</th>
                <th>Team</th>
                <th>Position</th>
                <th>Total Points</th>
                <th>Price</th>
            </tr>
            {rows}
        </table>
        <br>
        <a href="/" style="color: #ecf0f1;">⬅️ Back to Home</a>
    </body>
    </html>
    '''



@app.route("/api/teams", methods=["GET"])
def get_teams():
    response = requests.get(f"{FPL_BASE}/bootstrap-static/")
    if response.status_code == 200:
        data = response.json()
        teams = [{ "id": t["id"], "name": t["name"] } for t in data.get("teams", [])]

        rows = ""
        for team in teams:
            rows += f"<tr><td>{team['id']}</td><td>{team['name']}</td></tr>"

        return f'''
        <!DOCTYPE html>
        <html>
        <head>
            <title>FPL Teams</title>
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    background: linear-gradient(to right, #4b79a1, #283e51);
                    color: white;
                    text-align: center;
                    padding: 50px;
                }}
                table {{
                    margin: auto;
                    width: 60%;
                    border-collapse: collapse;
                    background-color: rgba(255, 255, 255, 0.1);
                    border-radius: 8px;
                    overflow: hidden;
                }}
                th, td {{
                    padding: 12px;
                    border-bottom: 1px solid #ddd;
                    color: white;
                }}
                th {{
                    background-color: #1abc9c;
                }}
            </style>
        </head>
        <body>
            <h1>🏟️ Premier League Teams</h1>
            <table>
                <tr><th>ID</th><th>Team Name</th></tr>
                {rows}
            </table>
            <br>
            <a href="/" style="color: #ecf0f1;">⬅️ Back to Home</a>
        </body>
        </html>
        '''
    return jsonify({"error": "Failed to fetch team data"}), 500

from datetime import datetime, timedelta

# 加在文件顶部（确保全局定义）
def get_team_mapping():
    try:
        response = requests.get(f"{FPL_BASE}/bootstrap-static/")
        if response.status_code == 200:
            teams = response.json().get("teams", [])
            return {t["id"]: t["name"] for t in teams}
    except:
        return {}
    return {}

@app.route("/api/fixtures", methods=["GET"])
def get_fixtures():
    response = requests.get(f"{FPL_BASE}/fixtures/")
    if response.status_code != 200:
        return jsonify({"error": "Failed to fetch fixture data"}), 500

    team_map = get_team_mapping()
    fixtures = response.json()

    now = datetime.utcnow()
    one_week_later = now + timedelta(days=7)

    def is_upcoming(fix):
        try:
            return fix.get("kickoff_time") and now <= datetime.fromisoformat(fix["kickoff_time"][:-1]) <= one_week_later
        except:
            return False

    upcoming = list(filter(is_upcoming, fixtures))[:10]

    rows = ""
    for f in upcoming:
        home = team_map.get(f.get("team_h"), f.get("team_h"))
        away = team_map.get(f.get("team_a"), f.get("team_a"))
        rows += f"""
        <tr>
            <td>{f.get("event")}</td>
            <td>{home}</td>
            <td>{away}</td>
            <td>{f.get("kickoff_time")}</td>
        </tr>
        """

    return f'''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Upcoming Fixtures</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
                background: linear-gradient(to right, #4b79a1, #283e51);
                color: white;
                text-align: center;
                padding: 50px;
            }}
            table {{
                margin: auto;
                width: 80%;
                border-collapse: collapse;
                background-color: rgba(255, 255, 255, 0.1);
                border-radius: 8px;
                overflow: hidden;
            }}
            th, td {{
                padding: 12px;
                border-bottom: 1px solid #ddd;
                color: white;
            }}
            th {{
                background-color: #1abc9c;
            }}
        </style>
    </head>
    <body>
        <h1>📅 Upcoming Fixtures (Next 7 Days)</h1>
        <table>
            <tr>
                <th>Gameweek</th>
                <th>Home Team</th>
                <th>Away Team</th>
                <th>Kickoff Time (UTC)</th>
            </tr>
            {rows}
        </table>
        <br>
        <a href="/" style="color: #ecf0f1;">⬅️ Back to Home</a>
    </body>
    </html>
    '''


