# core/background.py

import threading
import random
import time
import json
import os
import traceback

from core.comment_engine import generate_aether_comment
from core.activity_monitor import ActivityMonitor
from core.memory import Memory

# Globals to control monitor lifecycle
monitor_thread = None
monitor_running = False
chat_browser = None

def set_chat_browser(browser):
    """Links the main UI chatbox to the monitor engine."""
    global chat_browser
    chat_browser = browser

def start_monitoring():
    """Starts the activity monitor and idle comment thread."""
    global monitor_thread, monitor_running, monitor

    if monitor_running:
        print("[Aether Monitor] Already running. Skipping duplicate start.")
        return

    print("[Aether Monitor] Launching background monitor...")

    # Start the keyboard/mouse/app activity listener
    monitor = ActivityMonitor()
    monitor.start()

    # Start the random idle comment loop
    monitor_thread = threading.Thread(target=random_monitor_loop, daemon=True)
    monitor_thread.start()
    monitor_running = True

def random_monitor_loop():
    """Periodically summarizes recent user activity and generates an Aether comment."""
    global monitor_running
    try:
        while True:
            wait_minutes = random.randint(10, 35)
            print(f"[Aether Monitor] Waiting {wait_minutes} minutes...")
            time.sleep(wait_minutes * 60)

            try:
                if os.path.exists("activity_log.json"):
                    with open("activity_log.json", "r", encoding="utf-8") as f:
                        data = json.load(f)

                    if data:
                        comment = generate_aether_comment(data)

                        # Append to memory context
                        mem = Memory()
                        mem.add_turn("ai", comment)

                        # Display in chat
                        if chat_browser:
                            chat_browser.add_ai_message(comment)

                        # Reset log after comment
                        with open("activity_log.json", "w", encoding="utf-8") as f:
                            json.dump({}, f, indent=2)

            except Exception as e:
                print(f"[Aether Monitor] Error during random summary:\n{traceback.format_exc()}")

    finally:
        monitor_running = False
        print("[Aether Monitor] Monitor loop exited unexpectedly.")

def user_requested_activity_recall():
    """Allows the user to manually request an Aether-style comment from current activity log."""
    try:
        if not os.path.exists("activity_log.json"):
            return

        with open("activity_log.json", "r", encoding="utf-8") as f:
            data = json.load(f)

        if data:
            comment = generate_aether_comment(data)

            mem = Memory()
            mem.add_turn("ai", comment)

            if chat_browser:
                chat_browser.add_ai_message(comment)

            # Reset after manual recall
            with open("activity_log.json", "w", encoding="utf-8") as f:
                json.dump({}, f, indent=2)

    except Exception as e:
        print(f"[Aether Recall] Error during recall:\n{traceback.format_exc()}")
