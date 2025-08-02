import sys, os
from PyQt6.QtWidgets import QApplication
from PyQt6.QtGui import QIcon
from ui.chat_window import ChatWindow
from memory.memo_session import log_app_launch
from memory.memo_session import log_app_close


def main():
    app = QApplication(sys.argv)
    log_app_launch()
    app.aboutToQuit.connect(log_app_close)
    if sys.platform == "darwin":
        icon_path = os.path.abspath("assets/dockpic.png")
        app.setWindowIcon(QIcon(icon_path))

    chat_window = ChatWindow()
    chat_window.show()

    sys.exit(app.exec())

if __name__ == "__main__":
    main()

