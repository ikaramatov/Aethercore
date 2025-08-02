from PyQt6.QtWidgets import QMessageBox, QApplication
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt, QPoint
from popup.float import FloatingImageWindow


def center_widget_on_parent(widget, parent):
    if parent:
        parent_center = parent.geometry().center()
        global_center = parent.mapToGlobal(parent_center)
        widget.move(global_center - widget.rect().center())
    else:
        screen_geometry = widget.screen().geometry()
        widget.move(
            screen_geometry.center().x() - widget.width() // 2,
            screen_geometry.center().y() - widget.height() // 2
        )


def show_reboot_dialog(parent=None) -> bool:
    # 🖼️ Show floating Aether image
    image_window = FloatingImageWindow("assets/shocked_aether.png", width=400)
    image_window.show()
    QApplication.processEvents()
    screen = image_window.screen().geometry()
    image_window.move(
        screen.center().x() - image_window.width() // 2,
        screen.center().y() - image_window.height() // 2
    )

    # 🍏 Native macOS-style confirmation dialog
    box = QMessageBox(parent)
    box.setWindowTitle("Reboot Aether?")
    box.setText("Wipe her memory and start fresh?")
    pixmap = QPixmap("assets/reboot.png").scaled(96, 96, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
    box.setIconPixmap(pixmap)

    box.setStandardButtons(QMessageBox.StandardButton.Cancel | QMessageBox.StandardButton.Yes)
    box.setDefaultButton(QMessageBox.StandardButton.Yes)

    # 📍 Position dialog over parent (or screen center fallback)
    box.adjustSize()
    QApplication.processEvents()
    center_widget_on_parent(box, parent)

    result = box.exec()
    image_window.close()
    return result == QMessageBox.StandardButton.Yes
