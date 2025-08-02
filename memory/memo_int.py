import os
import json
from datetime import datetime, timedelta

# Constants
CACHE_DIR = "cache"
INTERACTIONS_FILE = os.path.join(CACHE_DIR, "interactions_log.json")
os.makedirs(CACHE_DIR, exist_ok=True)

# Known interactions
INTERACTIONS = {
    "/pinch": "User pinched the AI",
    "/poke": "User poked the AI",
    "/tap": "User tapped the AI",
    "/headpat": "User headpatted the AI",
    "/hug": "User hugged the AI",
    "/cuddle": "User cuddled with the AI",
    "/handshake": "User handshook the AI",
    "/highfive": "User highfived the AI",
    "/facepalm": "User facepalmed",
    "/ignore": "User ignored the AI",
    "/nod": "User nodded to the AI",
    "/bonk": "User bonked the AI",
    "/holdhand": "User held hands with the AI"
}

# Load JSON
def load_interactions():
    if os.path.exists(INTERACTIONS_FILE):
        with open(INTERACTIONS_FILE, "r") as f:
            return json.load(f)
    else:
        return {"total": {}, "daily": {}}

# Save JSON
def save_interactions(data):
    with open(INTERACTIONS_FILE, "w") as f:
        json.dump(data, f, indent=2)

# Format today's date
def get_date_string(date_obj):
    return date_obj.strftime("%Y-%m-%d")

# Log interaction
def log_interaction(command):
    if command not in INTERACTIONS:
        return  # Ignore unsupported commands

    today = get_date_string(datetime.today())
    yesterday = get_date_string(datetime.today() - timedelta(days=1))
    data = load_interactions()

    # Merge yesterday into total
    if yesterday in data["daily"]:
        for k, v in data["daily"][yesterday].items():
            data["total"][k] = data["total"].get(k, 0) + v
        del data["daily"][yesterday]

    # Init today
    if today not in data["daily"]:
        data["daily"][today] = {}

    # Count
    data["daily"][today][command] = data["daily"][today].get(command, 0) + 1
    save_interactions(data)

# Get summary string
def get_interaction_summary():
    today = get_date_string(datetime.today())
    data = load_interactions()
    daily = data.get("daily", {}).get(today, {})
    total = data.get("total", {})

    summary = []
    for cmd, description in INTERACTIONS.items():
        today_count = daily.get(cmd, 0)
        total_count = total.get(cmd, 0) + today_count
        summary.append(f"{description}: {today_count} times today, {total_count} times in total")
    return summary
