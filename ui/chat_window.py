from PyQt6.QtWidgets import QTextBrowser, QWidget, QPushButton, QVBoxLayout, QTextEdit, QLineEdit, QDialog
from PyQt6.QtCore import Qt, QTimer, QEvent
from PyQt6.QtGui import QTextCursor, QFont, QPalette, QColor
import random
from core.ai_engine import AIPersona
from core.chess_memory import ChessMemory
from ui.utils import append_colored_text, animate_typing
from games.chess import ChessGame
from popup.confirm_reboot import show_reboot_dialog
from popup.confirm_chess import show_chess_dialog
from popup.confirm_blackjack import show_blackjack_dialog
from core.memory import Memory
from popup.confirm_ttt import show_ttt_dialog
from games.tictactoe import TicTacToeGame
from games.blackjack import BlackjackGame


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


    def launch_chess_game(self):
        self.chess_window = ChessGame(send_comment_callback=self.render_aether_response)
        self.chess_window.game_closed_callback = self.aether_comment_on_exit  # 👈 This
        self.chess_window.show()
        
    def aether_comment_on_exit(self):
        simulated_input = "*I quit chess mid-game*"
        response = self.ai.generate_response(simulated_input)
        self.render_aether_response(response)

    
    def reboot_reaction(self):
        reaction = self.ai.generate_response("I rebooted you.")
        self.render_aether_response(reaction)
        
    def reset_chess_memory(self):
        mem = ChessMemory()
        mem.reset()

    def user_send(self):
        text = self.input_line.text().strip()
        if not text:
            return
        self.input_line.clear()

        # Handle Blackjack initiation
                # Handle blackjack initiation
        blackjack_phrases = [
            "play blackjack", "start blackjack", "let's play blackjack",
            "deal the cards", "i want to play blackjack", "blackjack time", "/blackjack"
        ]

        if any(phrase in text.lower() for phrase in blackjack_phrases):
            append_colored_text(self.chat_area, text, color="white")

            result = show_blackjack_dialog(self)
            if result:
                append_colored_text(self.chat_area, "*Æ shuffles the deck with a smirk* Let's play blackjack, dummy.")
                self.blackjack_window = BlackjackGame(send_comment_callback=self.render_aether_response)
                self.blackjack_window.show()
            else:
                append_colored_text(self.chat_area, "*Æ puts the cards back in the box, bored.* Another time then.")
            return
        
        # Handle Tic Tac Toe initiation
        if "tic tac toe" in text.lower() or text.strip().upper() == "TTT":
            append_colored_text(self.chat_area, text, color="white")

            result = show_ttt_dialog(self)
            if result:
                self.ttt_window = TicTacToeGame(send_comment_callback=self.render_aether_response)
                self.ttt_window.show()
                return
            else:
                append_colored_text(self.chat_area, "*Aether shrugs, mildly disappointed* Hmph. Maybe next time.")
            return
        
        # Handle chess initiation
        if "play chess" in text.lower():
            append_colored_text(self.chat_area, text, color="white")  # show user input
            
            result = show_chess_dialog(self)  # Show confirmation dialog

            if result:
                append_colored_text(self.chat_area, "*Aether grins mischievously* Alright, let's play~")
                self.launch_chess_game()
            else:
                append_colored_text(self.chat_area, "*Aether smirks and crosses her arms* Hmph. Backed out already?")
            return

        # Normal dialogue handling
        append_colored_text(self.chat_area, text, color="white")
        self.input_line.clear()
        self.reset_idle_timer()

        if text == "/reboot":
            result = show_reboot_dialog(self) 

            if result:
                system_lines = [
                    "system reboot initialized...",
                    "wiping memory...",
                    "cleaning contextual memory...",
                    "booting Aether...",
                    "system malfunction detected..."
                ]
                for i, line in enumerate(system_lines):
                    QTimer.singleShot(i * 800, lambda l=line: append_colored_text(self.chat_area, l, color="#FF4444"))  # vivid red

                QTimer.singleShot(len(system_lines) * 800 + 500, lambda: self.ai.reset_memory())
                QTimer.singleShot(len(system_lines) * 800 + 500, self.reset_chess_memory)  # 🧠💣 wipe chess too
                QTimer.singleShot(len(system_lines) * 800 + 1500, self.reboot_reaction)

            else:
                response = self.ai.generate_response("I almost rebooted you but changed my mind.")
                self.render_aether_response(response)
            return

        response = self.ai.generate_response(text)
        self.render_aether_response(response)

    def ai_initiate_talk(self):
        idle_comment = self.ai.idle_prompt()
        self.render_aether_response(idle_comment)
    
    def add_ai_message(self, message: str):
        self.chat_history.append(f"<b>Aether:</b> {message}")
