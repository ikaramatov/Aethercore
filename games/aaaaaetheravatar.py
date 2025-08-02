from PyQt6.QtWidgets import QLabel, QWidget
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt, QTimer, QCoreApplication
import os

class AetherAvatar(QWidget):
    def __init__(self, image_path):
        super().__init__()
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

        self.label = QLabel(self)
        self.set_avatar(image_path)

    def set_avatar(self, image_path):
        pixmap = QPixmap(image_path)

        # Scale pixmap to 50%
        scaled_pixmap = pixmap.scaled(
            pixmap.width() // 2,
            pixmap.height() // 2,
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation
        )

        self.label.setPixmap(scaled_pixmap)
        self.label.adjustSize()
        self.adjustSize()

        # Move to bottom-left of screen
        screen = QCoreApplication.instance().primaryScreen().availableGeometry()
        x = 0
        y = screen.height() - self.height()
        self.move(x, y)


