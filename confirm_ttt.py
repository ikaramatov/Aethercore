from PyQt6.QtWidgets import QMessageBox
from ui.base_confirm_dialog import FloatingImageWindow

def show_ttt_dialog(parent=None) -> bool:
    # 🖼️ Show floating image behind the dialog
    image_window = FloatingImageWindow("assets/aether_ttt.png", width=400)
    image_window.show()

    # 🧠 Native confirmation dialog
    box = QMessageBox(parent)
    box.setWindowTitle("Tic-Tac-Toe with Aether ✕○ XO")
    box.setText("Shall we play Tic-Tac-Toe?!")
    box.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.Cancel)
    box.setDefaultButton(QMessageBox.StandardButton.Cancel)
    box.setIcon(QMessageBox.Icon.Question)

    # ⚖️ Move dialog to center of the screen
    screen_geometry = box.screen().geometry()
    box.move(
        screen_geometry.center().x() - box.width() // 2,
        screen_geometry.center().y() - box.height() // 2
    )

    result = box.exec()
    image_window.close()

    return result == QMessageBox.StandardButton.Yes
