# main.py

import sys
import os
from PyQt6.QtWidgets import QApplication
from PyQt6.QtGui import QIcon

from ui.chat_window import ChatWindow
from core.activity_monitor import ActivityMonitor
from core import background

def main():
    app = QApplication(sys.argv)

    if sys.platform == "darwin":
        icon_path = os.path.abspath("assets/dockpic.png")
        app.setWindowIcon(QIcon(icon_path))

    chat_window = ChatWindow()
    chat_window.show()

    background.set_chat_browser(chat_window)
    background.start_monitoring()  # ✅ this is enough

    sys.exit(app.exec())

if __name__ == "__main__":
    main()
