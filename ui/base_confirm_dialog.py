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

        label = QLabel(self)
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # 🧠 Scale the pixmap BEFORE setting
        pixmap = QPixmap(image_path)
        scaled_pixmap = pixmap.scaledToWidth(width, Qt.TransformationMode.SmoothTransformation)
        label.setPixmap(scaled_pixmap)

        # 🧠 Prevent QLabel from growing unexpectedly
        label.setFixedSize(scaled_pixmap.size())

        layout.addWidget(label)
        self.setLayout(layout)

        # 🧠 Fix the dialog size to match the image
        self.setFixedSize(scaled_pixmap.size())

    def center_on_screen(self):
        screen = self.screen().geometry()
        self.move(
            screen.center().x() - self.width() // 2,
            screen.center().y() - self.height() // 2 - 60  # a bit above center
        )
