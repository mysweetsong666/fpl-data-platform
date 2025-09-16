import requests
from app import db, Player, app

url = "https://fantasy.premierleague.com/api/bootstrap-static/"

def fetch_fpl_players():
    with app.app_context():
        db.create_all()
        res = requests.get(url)
        data = res.json()
        for p in data["elements"]:
            player = Player(
                id=p["id"],
                name=p["web_name"],
                team=str(p["team"]),
                total_points=p["total_points"],
                price=p["now_cost"] / 10
            )
            db.session.merge(player)
        db.session.commit()

if __name__ == "__main__":
    fetch_fpl_players()
