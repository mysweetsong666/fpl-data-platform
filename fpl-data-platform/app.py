from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

FPL_BASE = "https://fantasy.premierleague.com/api"

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
    if response.status_code == 200:
        data = response.json()
        players = [
            {
                "name": f"{p['first_name']} {p['second_name']}",
                "team_id": p["team"],
                "position": p["element_type"],
                "total_points": p["total_points"]
            }
            for p in data.get("elements", [])[:20]
        ]
        return jsonify(players)
    return jsonify({"error": "Failed to fetch player data"}), 500

@app.route("/api/teams", methods=["GET"])
def get_teams():
    response = requests.get(f"{FPL_BASE}/bootstrap-static/")
    if response.status_code == 200:
        data = response.json()
        teams = [{ "id": t["id"], "name": t["name"] } for t in data.get("teams", [])]
        return jsonify(teams)
    return jsonify({"error": "Failed to fetch team data"}), 500

@app.route("/api/fixtures", methods=["GET"])
def get_fixtures():
    response = requests.get(f"{FPL_BASE}/fixtures/")
    if response.status_code == 200:
        fixtures = response.json()[:20]
        simplified = [
            {
                "event": f.get("event"),
                "team_h": f.get("team_h"),
                "team_a": f.get("team_a"),
                "kickoff_time": f.get("kickoff_time")
            }
            for f in fixtures
        ]
        return jsonify(simplified)
    return jsonify({"error": "Failed to fetch fixtures"}), 500
