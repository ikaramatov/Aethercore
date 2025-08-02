from PyQt6.QtWidgets import QTextBrowser, QWidget, QPushButton, QVBoxLayout, QTextEdit, QLineEdit, QDialog
from PyQt6.QtCore import Qt, QTimer, QEvent
from PyQt6.QtGui import QTextCursor, QFont, QPalette, QColor
import random
from core.ai_engine import AIPersona
from core.chess_memory import ChessMemory
from ui.utils import append_colored_text, animate_typing
from games.chess import ChessGame
from core.memory import Memory
from ui.shortkeys import HandleShortkeys


memory = Memory()

class ChatWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Aethercore 2.0 💻")
        self.setGeometry(200, 200, 500, 600)
        
        self.setWindowFlags(self.windowFlags() | Qt.WindowType.WindowStaysOnTopHint)
        self.show()  # re-show to apply new flags if needed
        
        self.setAutoFillBackground(True)
        palette = QPalette()
        palette.setColor(QPalette.ColorRole.Window, QColor("#1E1E1E"))  # unified dark grey
        self.setPalette(palette)
        self.old_pos = None
        self.ai = AIPersona()
        self.chess_window = None
        
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)  # ⬅️ no external spacing
        self.layout.setSpacing(0)
        self.chat_area = QTextEdit()
        self.chat_area.setReadOnly(True)
        self.chat_area.setFont(QFont("FiraCode Nerd Font", 14))
        self.chat_area.setStyleSheet("""
            QTextEdit {
                background-color: #1E1E1E;
                color: white;
                border: none;
                padding: 0px;
            }
            QScrollBar:vertical {
                width: 0px;
                background: transparent;
            }
            QScrollBar::handle:vertical {
                width: 0px;
                background: transparent;
            }
            QScrollBar::add-line:vertical,
            QScrollBar::sub-line:vertical,
            QScrollBar::up-arrow:vertical,
            QScrollBar::down-arrow:vertical {
                height: 0px;
                width: 0px;
                background: none;
            }
        """)
        
        self.generating = False
        self.current_animation_timer = None
        
        self.chat_area.installEventFilter(self)        
        self.input_line = QLineEdit()
        self.input_line.setFont(QFont("FiraCode Nerd Font", 14))
        self.input_line.setStyleSheet("background-color: #2A2A2A; color: white; padding: 6px; border: none;")
        
        #STOP GENERATING
        self.stop_button = QPushButton("■", self.input_line)
        self.stop_button.setStyleSheet("""
            QPushButton {
                background-color: #AA0000;
                color: white;
                font-weight: bold;
                border: none;
                font-size: 12px;
            }
        """)
        self.stop_button.setFixedSize(20, 20)
        self.stop_button.move(self.input_line.width() - 24, (self.input_line.height() - 20) // 2)
        self.stop_button.hide()
        self.stop_button.clicked.connect(self.stop_generation)

        # Optional: Add spacing on the right of input to not hide text under button
        self.input_line.setStyleSheet("""
            background-color: #2A2A2A;
            color: white;
            padding: 6px;
            padding-right: 30px;  /* Leave room for red square */
            border: none;
        """)

        # Ensure button repositions if input_line resizes
        self.input_line.resizeEvent = self.reposition_stop_button


        # LAYOUT
        self.layout.addWidget(self.chat_area)
        self.layout.addWidget(self.input_line)
        self.setLayout(self.layout)

        self.input_line.returnPressed.connect(self.user_send)

        # Idle timer
        self.idle_timer = QTimer()
        self.idle_timer.timeout.connect(self.ai_initiate_talk)
        self.reset_idle_timer()

    def append_message(self, sender, message):
        self.append(f"<b>{sender}:</b> {message}")
    
    def reposition_stop_button(self, event):
        self.stop_button.move(self.input_line.width() - 24, (self.input_line.height() - 20) // 2)
        event.accept()
    
    def stop_generation(self):
        self.stop_requested = True
        if self.current_animation_timer:
            self.current_animation_timer.stop()
        self.finish_generation()

    def finish_generation(self):
        self.generating = False
        self.stop_button.hide()
        self.stop_requested = False
    
    def reset_idle_timer(self):
        delay = random.choice([180000, 350000, 840000, 1980000])  # ms
        self.idle_timer.start(delay)

    def render_aether_response(self, text: str):
        if "*" not in text:
            animate_typing(self.chat_area, text.strip(), color="#FF69B4", chat_window=self)
            return

        parts = text.split("*")
        for i, part in enumerate(parts):
            if not part.strip():
                continue

            if i % 2 == 0:
                animate_typing(self.chat_area, part.strip(), color="#FF69B4", chat_window=self)  # Dialogue
            else:
                append_colored_text(self.chat_area, part.strip(), color="#888888")  # Action

        
    def reset_chess_memory(self):
        mem = ChessMemory()
        mem.reset()


    def user_send(self):
        text = self.input_line.text().strip()
        if not text:
            return

        self.input_line.clear()
        append_colored_text(self.chat_area, text, color="white")
        self.reset_idle_timer()

        if text.startswith("/"):
            if HandleShortkeys.handle_input(self, text):
                return

        # fallback to AI
        response = self.ai.generate_response(text)
        self.render_aether_response(response)


    def ai_initiate_talk(self):
        idle_comment = self.ai.idle_prompt()
        self.render_aether_response(idle_comment)
    
    def add_ai_message(self, message: str):
        self.chat_history.append(f"<b>Aether:</b> {message}")
