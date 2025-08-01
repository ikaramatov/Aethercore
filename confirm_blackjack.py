from PyQt6.QtWidgets import QMessageBox
from ui.base_confirm_dialog import FloatingImageWindow


def show_blackjack_dialog(parent=None) -> bool:
    # 🖼️ Show floating image of Aether with cards
    image_window = FloatingImageWindow("assets/aether_blackjack.png", width=400)
    image_window.show()

    # 🧠 Native confirmation dialog
    box = QMessageBox(parent)
    box.setWindowTitle("Play Blackjack with Aether 🃏")
    box.setText("Let me deal you?")
    box.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.Cancel)
    box.setDefaultButton(QMessageBox.StandardButton.Cancel)
    box.setIcon(QMessageBox.Icon.Question)

    # ⚖️ Center the dialog on screen
    screen_geometry = box.screen().geometry()
    box.move(
        screen_geometry.center().x() - box.width() // 2,
        screen_geometry.center().y() - box.height() // 2
    )

    result = box.exec()
    image_window.close()

    return result == QMessageBox.StandardButton.Yes
