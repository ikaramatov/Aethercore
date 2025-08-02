import json, os
from datetime import datetime

class MemoryLog:
    def __init__(self, path="memory.json"):
        self.path = path
        self.data = {}
        self._load()

    def _load(self):
        if os.path.exists(self.path):
            try:
                with open(self.path, "r", encoding="utf-8") as f:
                    self.data = json.load(f)
            except Exception:
                self.data = {}
        else:
            self.data = {}

    def append_to_log(self, topic, message):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        if topic not in self.data:
            self.data[topic] = []
        self.data[topic].append({"time": timestamp, "message": message})
        self._save()

    def _save(self):
        with open(self.path, "w", encoding="utf-8") as f:
            json.dump(self.data, f, indent=2, ensure_ascii=False)

    def get_log(self, topic):
        return self.data.get(topic, [])



class Memory:
    def __init__(self, filename="memory.json"):
        self.memory_file = os.path.abspath(filename)
        self.history = []

        if os.path.exists(self.memory_file):
            try:
                with open(self.memory_file, "r", encoding="utf-8") as f:
                    self.history = json.load(f)
            except json.JSONDecodeError:
                self.history = []

    def add_turn(self, role: str, text: str):
        self.history.append((role, text))
        if len(self.history) > 100:
            self.history.pop(0)
        self.save()
        if role == "user":
            self.update_last_seen()

    def update_last_seen(self):
        with open("last_seen.json", "w", encoding="utf-8") as f:
            json.dump({"last_seen": datetime.now().isoformat()}, f)

    def get_context(self):
        return [f"{role}: {text}" for role, text in self.history]

    def clear(self):
        self.history = []
        self.save()

    def save(self):
        with open(self.memory_file, "w", encoding="utf-8") as f:
            json.dump(self.history, f, ensure_ascii=False, indent=2)

    def load(self):
        if os.path.exists(self.memory_file):
            with open(self.memory_file, "r", encoding="utf-8") as f:
                self.history = json.load(f)

    def summarize_history(self):
        last_10 = self.history[-10:]
        lines = [f"{role}: {text}" for role, text in last_10]
        return " | ".join(lines)
