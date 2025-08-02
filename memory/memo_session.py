import os
import json
from datetime import datetime, timedelta

CACHE_DIR = "cache"
SESSION_FILE = os.path.join(CACHE_DIR, "session.json")
os.makedirs(CACHE_DIR, exist_ok=True)

def _load_session_data():
    if os.path.exists(SESSION_FILE):
        with open(SESSION_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    else:
        return {
            "launch": {
                "total": 0,
                "daily": {}
            },
            "duration_minutes": {
                "total": 0,
                "last": 0
            },
            "last_ended_at": None
        }

def _save_session_data(data):
    with open(SESSION_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

def _get_today():
    return datetime.today().strftime("%Y-%m-%d")

# 🔁 Log app launch
def log_app_launch():
    now = datetime.now()
    data = _load_session_data()
    today = _get_today()

    # Launch counters
    data["launch"]["total"] += 1
    data["launch"]["daily"][today] = data["launch"]["daily"].get(today, 0) + 1

    # Track current session start
    data["_active_session_start"] = now.isoformat()
    _save_session_data(data)

# ✅ Log app close (session end)
def log_app_close():
    data = _load_session_data()
    now = datetime.now()

    start_str = data.get("_active_session_start")
    if start_str:
        start_time = datetime.fromisoformat(start_str)
        duration = max((now - start_time).total_seconds() / 60, 0)
    else:
        duration = 0

    data["duration_minutes"]["last"] = round(duration)
    data["duration_minutes"]["total"] += round(duration)
    data["last_ended_at"] = now.isoformat()

    data.pop("_active_session_start", None)  # Clean up

    _save_session_data(data)

# 📊 Get human-readable summary
def get_session_summary():
    data = _load_session_data()
    today = _get_today()
    now = datetime.now()

    launches_today = data["launch"]["daily"].get(today, 0)
    launches_total = data["launch"]["total"]

    last_duration = data["duration_minutes"]["last"]
    total_duration = data["duration_minutes"]["total"]

    ended_at = data.get("last_ended_at")
    if ended_at:
        ended_time = datetime.fromisoformat(ended_at)
        minutes_ago = max(int((now - ended_time).total_seconds() / 60), 0)
    else:
        minutes_ago = "unknown"

    return [
        f"User has launched the app {launches_today} time(s) today, {launches_total} time(s) in total.",
        f"Last session's duration: {last_duration} minute(s), {total_duration} minute(s) in total.",
        f"Last session ended {minutes_ago} minute(s) ago."
    ]
