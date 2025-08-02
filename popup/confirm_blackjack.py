from PyQt6.QtWidgets import QMessageBox
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import QFile, QTextStream
from popup.float import FloatingImageWindow


def load_confirm_style() -> str:
    file = QFile("popup/confirm_layout.qss")
    if file.open(QFile.OpenModeFlag.ReadOnly | QFile.OpenModeFlag.Text):
        return QTextStream(file).readAll()
    return ""


def show_blackjack_dialog(parent=None) -> bool:
    # 🎴 Floating Aether image
    image_window = FloatingImageWindow("assets/aether_blackjack.png", width=400)
    image_window.show()

    # 🃏 Confirmation dialog
    box = QMessageBox(parent)
    box.setWindowTitle("Blackjack with Aether ♦️♠️")
    box.setText("Do you dare to play Blackjack?")
    box.setIconPixmap(QIcon("assets/blackjack_icon.png").pixmap(64, 64))  # Custom icon
    box.setStandardButtons(QMessageBox.StandardButton.Cancel | QMessageBox.StandardButton.Yes)
    box.setDefaultButton(QMessageBox.StandardButton.Yes)

    # 🎨 Apply custom QSS
    box.setStyleSheet(load_confirm_style())

    # 🧭 Center the dialog
    screen_geometry = box.screen().geometry()
    box.move(
        screen_geometry.center().x() - box.width() // 2,
        screen_geometry.center().y() - box.height() // 2
    )

    result = box.exec()
    image_window.close()

    return result == QMessageBox.StandardButton.Yes
