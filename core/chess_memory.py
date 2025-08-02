import os, json
from datetime import datetime

MEMORY_FILE = "chess_memory.json"


class ChessMemory:
    def __init__(self):
        self.data = {
            "fen": "startpos",
            "last_move": None,
            "game_active": False,
            "move_history": [],
            "started_at": None,
            "ended_at": None,
            "result": None,
            "aether_comment": None
        }
        self._load()

    def _load(self):
        if os.path.exists(MEMORY_FILE):
            try:
                with open(MEMORY_FILE, "r", encoding="utf-8") as f:
                    self.data = json.load(f)
            except (json.JSONDecodeError, IOError):
                print("⚠️ Could not load chess memory. Starting fresh.")
                self.save()
        else:
            self.save()

    def save(self):
        try:
            with open(MEMORY_FILE, "w", encoding="utf-8") as f:
                json.dump(self.data, f, indent=4)
        except IOError:
            print("⚠️ Failed to save chess memory.")
            
    def update_fen(self, fen):
        self.data["fen"] = fen
        self.save()

    def start_game(self, fen="startpos"):
        self.data.update({
            "fen": fen,
            "last_move": None,
            "move_history": [],
            "game_active": True,
            "started_at": datetime.now().isoformat(),
            "ended_at": None,
            "result": None,
            "aether_comment": None
        })
        self.save()

    def record_move(self, move_uci, fen):
        self.data["last_move"] = move_uci
        self.data["move_history"].append(move_uci)
        self.data["fen"] = fen
        self.save()

    def end_game(self, result, comment=None):
        self.data["game_active"] = False
        self.data["result"] = result
        self.data["ended_at"] = datetime.now().isoformat()
        if comment:
            self.data["aether_comment"] = comment
        self.save()


    def reset(self):
        self.data = {
            "fen": "startpos",
            "last_move": None,
            "game_active": False,
            "move_history": [],
            "started_at": None,
            "ended_at": None,
            "result": None,
            "aether_comment": None
        }
        self.save()


    def is_active(self):
        return self.data.get("game_active", False)

    def get_fen(self):
        return self.data.get("fen", "startpos")

    def get_move_history(self):
        return self.data.get("move_history", [])

    def get_last_comment(self):
        return self.data.get("aether_comment", None)
