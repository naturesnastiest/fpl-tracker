import os
import requests
from flask import Flask, jsonify, send_from_directory
from flask_cors import CORS

app = Flask(__name__, static_folder="static")
CORS(app)

FPL_EMAIL = os.environ.get("FPL_EMAIL")
FPL_PASSWORD = os.environ.get("FPL_PASSWORD")
LEAGUE_ID = os.environ.get("LEAGUE_ID", "86512")

DRAFT_BASE = "https://draft.premierleague.com/api"
FPL_BASE = "https://fantasy.premierleague.com/api"

LOGIN_URL = "https://users.premierleague.com/accounts/login/"

def get_session():
    """Create an authenticated session with FPL."""
    session = requests.Session()
    session.headers.update({
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36",
        "Referer": "https://draft.premierleague.com/",
        "Origin": "https://draft.premierleague.com",
    })

    # Get login page first to grab CSRF token
    session.get("https://draft.premierleague.com/")

    payload = {
        "login": FPL_EMAIL,
        "password": FPL_PASSWORD,
        "app": "pldraft",
        "redirect_uri": "https://draft.premierleague.com/",
    }

    resp = session.post(LOGIN_URL, data=payload, allow_redirects=True)
    if resp.status_code not in (200, 302):
        raise Exception(f"Login failed with status {resp.status_code}")

    return session


@app.route("/api/league")
def get_league():
    try:
        session = get_session()

        # Fetch league details
        league_resp = session.get(f"{DRAFT_BASE}/league/{LEAGUE_ID}/details")
        if league_resp.status_code != 200:
            return jsonify({"error": f"Could not fetch league: HTTP {league_resp.status_code}"}), 500
        league_data = league_resp.json()

        # Fetch current gameweek from main FPL API (no auth needed)
        gw_resp = requests.get(f"{FPL_BASE}/bootstrap-static/")
        bootstrap = gw_resp.json()
        current_gw = next(
            (e["id"] for e in bootstrap["events"] if e.get("is_current")),
            next((e["id"] for e in bootstrap["events"] if e.get("finished")), None)
        )

        return jsonify({
            "league": league_data,
            "current_gw": current_gw
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/")
def index():
    return send_from_directory("static", "index.html")


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
