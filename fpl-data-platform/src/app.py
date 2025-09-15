from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

FPL_BASE = "https://fantasy.premierleague.com/api"

@app.route("/", methods=["GET"])
def index():
    return '''
        <h2>FPL Data Analysis Platform</h2>
        <form action="/echo_user_input" method="POST">
            Enter your favorite FPL player: <input name="user_input">
            <input type="submit" value="Submit">
        </form>
        <p>See: <a href="/api/players">/api/players</a> | <a href="/api/teams">/api/teams</a> | <a href="/api/fixtures">/api/fixtures</a></p>
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
