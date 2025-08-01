import json
import threading
import time
import random
from datetime import datetime
from pynput import keyboard, mouse
import psutil
import os
from core.comment_engine import generate_aether_comment

ACTIVITY_LOG = "activity_log.json"

class ActivityMonitor:
    def __init__(self):
        self.lock = threading.Lock()
        self.reset_log()

    def reset_log(self):
        self.activity = {
            "key_presses": 0,
            "mouse_clicks": 0,
            "mouse_moves": 0,
            "active_apps": set()
        }

    def _on_key_press(self, key):
        with self.lock:
            self.activity["key_presses"] += 1

    def _on_click(self, x, y, button, pressed):
        if pressed:
            with self.lock:
                self.activity["mouse_clicks"] += 1

    def _on_move(self, x, y):
        with self.lock:
            self.activity["mouse_moves"] += 1

    def _get_active_window_titles(self):
        titles = set()
        for proc in psutil.process_iter(['name']):
            try:
                name = proc.info['name']
                if name:
                    titles.add(name)
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue
        return titles

    def _log_activity(self):
        with self.lock:
            self.activity["active_apps"] = list(self._get_active_window_titles())
            with open(ACTIVITY_LOG, "w", encoding="utf-8") as f:
                json.dump(self.activity, f, indent=2, ensure_ascii=False)

    def _summarize_and_comment(self):
        with self.lock:
            self.activity["active_apps"] = list(self.activity["active_apps"])
            summary = self.activity.copy()
            comment = generate_aether_comment(summary)
            self.reset_log()  # 🔄 Reset for next loop
            return comment

    def _monitor_loop(self):
        while True:
            duration = random.choice([600, 900, 1200, 1500, 1800, 2100])  # ⏱️ Randomized
            print(f"[Aether Monitor] Waiting {duration // 60} minutes...")
            time.sleep(duration)

            self._log_activity()
            comment = self._summarize_and_comment()

            from core import background  # 🔁 Circular import workaround
            if background.chat_browser:
                background.chat_browser.render_aether_response(comment)

    def start(self):
        threading.Thread(target=self._monitor_loop, daemon=True).start()
        keyboard.Listener(on_press=self._on_key_press).start()
        mouse.Listener(on_click=self._on_click, on_move=self._on_move).start()
