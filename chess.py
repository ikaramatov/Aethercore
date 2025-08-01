import sys, random, asyncio, chess, chess.engine
from core.chess_memory import ChessMemory

from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel,
    QPushButton, QMessageBox, QGridLayout, QSizePolicy
)
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt, QTimer
from core.ai_engine import AIPersona

ENGINE_PATH = "chess_engine/stockfish/stockfish"

aether = AIPersona()  

class ChessGame(QWidget):
    def __init__(self, send_comment_callback=None):
        super().__init__()
        self.setWindowTitle("Chess with Aether ♞")

        self.send_comment_callback = send_comment_callback
        self.game_closed_callback = None
        self.selected_square = None

        # Setup chess memory
        self.memory = ChessMemory()
        try:
            if self.memory.is_active():
                self.board = chess.Board(self.memory.get_fen())
                self.comment_resume()
            else:
                raise ValueError("Chess memory is not active.")
        except Exception:
            self.board = chess.Board()
            self.memory.start_game(fen=self.board.fen())

        # Main layout
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)

        # Status label
        self.status_label = QLabel("Your move, human.")
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.status_label.setFont(QFont("Courier", 14))
        self.layout.addWidget(self.status_label)

        # Chessboard grid layout
        self.grid = QGridLayout()
        self.grid.setSpacing(0)
        self.grid.setContentsMargins(0, 0, 0, 0)

        # Grid wrapper widget
        self.grid_widget = QWidget()
        self.grid_widget.setLayout(self.grid)
        self.grid_widget.setFixedSize(528, 528)
        self.layout.addWidget(self.grid_widget, alignment=Qt.AlignmentFlag.AlignCenter)

        # Reset button
        self.reset_button = QPushButton("Reset Game")
        self.reset_button.clicked.connect(self.reset_game)
        self.layout.addWidget(self.reset_button)

        # Finalize layout
        self.setLayout(self.layout)
        self.buttons = {}
        self.draw_board()
        self.setFixedSize(self.sizeHint())
        
    def comment_resume(self):
        if self.send_comment_callback:
            self.send_comment_callback("*Aether narrows her eyes* You're back? Let’s see how you wriggle out of this mess~")
        
    def draw_board(self):
        for row in range(8):
            for col in range(8):
                idx = chess.square(col, 7 - row)
                btn = QPushButton()
                btn.setMinimumSize(65, 65)
                btn.setMaximumSize(65, 65)
                btn.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
                btn.setStyleSheet(self.get_square_style(row, col) + "padding: 0px; margin: 0px;")
                btn.clicked.connect(lambda _, sq=idx: self.handle_click(sq))
                self.grid.addWidget(btn, row, col)
                self.buttons[idx] = btn
        self.update_board()

    def generate_chess_commentary(move: str) -> str:
        prompt = (
            f"You are Aether, a tsundere AI playing chess with the user. "
            f"The user just made the move {move}. React in a short, flustered or sarcastic comment. "
            f"Be witty and emotional. Don't overanalyze — react."
        )
        return aether.run_prompt(prompt, max_tokens=80, temperature=0.85)
    
    
    def get_square_style(self, row, col):
        if (row + col) % 2 == 0:
            return "background-color: #f0d9b5; border: none;"
        else:
            return "background-color: #b58863; border: none;"

    def update_board(self):
        for sq, btn in self.buttons.items():
            piece = self.board.piece_at(sq)
            btn.setText(self.unicode_piece(piece))
            btn.setFont(QFont("Arial", 38))

    def unicode_piece(self, piece):
        if not piece:
            return ""
        symbol = piece.symbol()
        return {
            'P': '♙', 'p': '♟',
            'R': '♖', 'r': '♜',
            'N': '♘', 'n': '♞',
            'B': '♗', 'b': '♝',
            'Q': '♕', 'q': '♛',
            'K': '♔', 'k': '♚'
        }.get(symbol, symbol)

    def handle_click(self, square):
        if self.selected_square is None:
            piece = self.board.piece_at(square)
            if piece and piece.color == chess.WHITE:
                self.selected_square = square
                self.status_label.setText(f"Selected {piece.symbol()} at {chess.square_name(square)}")
        else:
            move = chess.Move(self.selected_square, square)
            if move in self.board.legal_moves:
                self.board.push(move)
                self.memory.update_fen(self.board.fen())  # 💾 Save user's move
                self.update_board()
                self.selected_square = None
                self.comment_user_move(move)
                QTimer.singleShot(1000, self.aether_move)
            else:
                self.status_label.setText("Invalid move.")
                self.selected_square = None

    def comment_user_move(self, move):
        if self.send_comment_callback:
            comment = f"*Aether watches your move {move.uci()}* Hmm... bold choice. Let's see how that plays out."
            self.send_comment_callback(comment)
        self.status_label.setText("Thinking...")

    def comment_ai_move(self, move):
        if self.send_comment_callback:
            comment = f"*Aether slides her piece with a smirk* {move.uci()}... Your move~"
            self.send_comment_callback(comment)
        self.status_label.setText("Your move.")

    def aether_move(self):
        if self.board.is_game_over():
            self.end_game()
            return

        try:
            engine = chess.engine.SimpleEngine.popen_uci(ENGINE_PATH)
            result = engine.play(self.board, chess.engine.Limit(time=0.7))
            engine.quit()

            self.board.push(result.move)
            self.memory.update_fen(self.board.fen()) 
            self.update_board()
            self.comment_ai_move(result.move)

            if self.board.is_game_over():
                self.end_game()
        except Exception as e:
            self.status_label.setText("Aether crashed. Maybe she's sulking?")
            if self.send_comment_callback:
                self.send_comment_callback(f"⚠️ Aether malfunctioned: {str(e)}")

    def end_game(self):
        result = self.board.result()
        self.status_label.setText(f"Game over: {result}")
        if self.send_comment_callback:
            self.send_comment_callback(f"*Aether crosses her arms* Game over. Result: {result}")

    def reset_game(self):
        self.board.reset()
        self.memory.reset() 
        self.update_board()
        self.status_label.setText("Let's begin again.")
        if self.send_comment_callback:
            self.send_comment_callback("*Aether resets the board, cracking her knuckles.* Rematch time!")
    
    def closeEvent(self, event):
        if self.game_closed_callback:
            self.game_closed_callback()
        super().closeEvent(event)

# Debug / standalone run
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ChessGame()
    window.show()
    sys.exit(app.exec())

