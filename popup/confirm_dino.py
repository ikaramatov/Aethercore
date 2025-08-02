from PyQt6.QtWidgets import QMessageBox
from PyQt6.QtCore import QFile, QTextStream
from popup.float import FloatingImageWindow

def load_confirm_style() -> str:
    file = QFile("popup/confirm_layout.qss")
    if file.open(QFile.OpenModeFlag.ReadOnly | QFile.OpenModeFlag.Text):
        return QTextStream(file).readAll()
    return ""

def show_dino_dialog(parent=None) -> bool:
    image_window = FloatingImageWindow("assets/aether_dino.png", width=400)
    image_window.show()

    box = QMessageBox(parent)
    box.setWindowTitle("Dino Run 🦖💨")
    box.setText("Wanna dodge some cacti together?")
    box.setIconPixmap("assets/dino.png")  # custom PNG icon
    box.setStandardButtons(QMessageBox.StandardButton.Cancel | QMessageBox.StandardButton.Yes)
    box.setDefaultButton(QMessageBox.StandardButton.Yes)
    box.setStyleSheet(load_confirm_style())

    screen_geometry = box.screen().geometry()
    box.move(
        screen_geometry.center().x() - box.width() // 2,
        screen_geometry.center().y() - box.height() // 2
    )

    result = box.exec()
    image_window.close()
    return result == QMessageBox.StandardButton.Yes
