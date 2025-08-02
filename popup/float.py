from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt


class FloatingImageWindow(QDialog):
    def __init__(self, image_path: str, width: int = 350):
        super().__init__()
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint |
            Qt.WindowType.WindowStaysOnTopHint |
            Qt.WindowType.Tool  # hides from taskbar
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)

        label = QLabel()
        pixmap = QPixmap(image_path)
        pixmap = pixmap.scaledToWidth(width, Qt.TransformationMode.SmoothTransformation)
        label.setPixmap(pixmap)

        layout.addWidget(label)
        self.setLayout(layout)

    def center_on_screen(self):
        screen = self.screen().geometry()
        self.move(
            screen.center().x() - self.width() // 2,
            screen.center().y() - self.height() // 2
        )
