from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QGridLayout, QSizePolicy, QPushButton
from PyQt6.QtCore import Qt, QCoreApplication, QTimer, QSize, QUrl
from PyQt6.QtGui import QFont, QPixmap, QIcon, QCursor
from PyQt6.QtMultimedia import QSoundEffect
import os
from games.aetheravatar import AetherAvatar

class TicTacToeGame(QWidget):
    def __init__(self, send_comment_callback=None):
        super().__init__()
        self.setWindowTitle("Tic-Tac-Toe with Aether ❌⭕")
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint |
            Qt.WindowType.WindowStaysOnTopHint
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.container = QWidget(self)
        
        self.send_comment_callback = send_comment_callback
        self.avatar = AetherAvatar("assets/aether_idle.png")
        self.avatar.show()

        self.current_player = "X"
        self.board = [[None for _ in range(3)] for _ in range(3)]
        self.scores = {"ME": 0, "Æ": 0}
        
        self.click_sound = QSoundEffect()
        self.click_sound.setSource(QUrl.fromLocalFile(os.path.join(
            QCoreApplication.applicationDirPath(), "assets/click.wav")))
        
        # main layout
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        
        # Background
        paper_path = "assets/TTT_window.png"
        self.bg_label = QLabel(self)
        if os.path.exists(paper_path):
            pixmap = QPixmap(paper_path).scaledToWidth(
                2 * QPixmap(paper_path).width(), Qt.TransformationMode.SmoothTransformation
            )
            self.bg_label.setPixmap(pixmap)
            self.bg_label.setScaledContents(True)
            self.bg_label.setFixedSize(pixmap.size())
            self.setFixedSize(pixmap.size())

        main_layout.addWidget(self.bg_label)
        
        # Quit button (bottom right of paper)
        self.quit_button = QPushButton(self.bg_label)
        self.quit_button.setIcon(QIcon("assets/quit.png"))
        self.quit_button.setIconSize(QSize(72, 72))
        self.quit_button.setStyleSheet("background-color: transparent; border: none;")
        self.quit_button.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        # Position manually
        self.quit_button.move(self.bg_label.width() - 90, self.bg_label.height() - 70)
        self.quit_button.clicked.connect(self.close)
        self.quit_button.clicked.connect(self.quit_game)

        
        # Center screen
        screen = QCoreApplication.instance().primaryScreen().availableGeometry()
        x = (screen.width() - self.width()) // 2
        y = (screen.height() - self.height()) // 2
        self.move(x, y)
        
        # Grid overlay
        self.grid = QGridLayout(self.bg_label)
        self.grid.setContentsMargins(100, 120, 100, 100)
        self.grid.setSpacing(0)
        
        #Score label
        self.score_label = QLabel("ME: 0  vs  Æ: 0", self.bg_label)
        self.score_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.score_label.setFont(QFont("FiraCode Nerd Font", 48, QFont.Weight.Bold))
        self.score_label.setStyleSheet("color: black; padding-bottom: 30px; padding-top: 20px")
        self.grid.addWidget(self.score_label, 0, 0, 1, 3, alignment=Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter)
    
        #game buttons
        self.buttons = {}
        for row in range(3):
            for col in range(3):
                btn = QPushButton()
                btn.setFixedSize(160, 160)
                btn.setStyleSheet("background-color: transparent;")
                btn.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
                btn.setIconSize(QSize(160, 160))
                btn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
                self.grid.addWidget(btn, row + 1, col)
                self.buttons[(row, col)] = btn

                def make_handler(r=row, c=col):
                    return lambda: self.handle_click(r, c)
                btn.clicked.connect(make_handler())

                def make_enter(r=row, c=col):
                    return lambda _: self.show_preview(r, c)

                def make_leave(r=row, c=col):
                    return lambda _: self.clear_preview(r, c)

                btn.enterEvent = make_enter()
                btn.leaveEvent = make_leave()
                
    def quit_game(self):
        if self.send_comment_callback:
            self.send_comment_callback("Æ: Hmph, running away already?")
        self.avatar.close()
        self.close()

    def handle_click(self, row, col):
        if self.board[row][col] is not None or self.current_player != "X":
            return

        self.make_move(row, col, "X")
        winner = self.check_winner()
        if winner:
            self.process_winner(winner)
            return

        if self.is_draw():
            QTimer.singleShot(2000, self.reset_board)
            return

        self.current_player = "O"
        QTimer.singleShot(500, self.ai_move)

    def ai_move(self):
        best_score = -float('inf')
        best_move = None

        for row in range(3):
            for col in range(3):
                if self.board[row][col] is None:
                    self.board[row][col] = "O"
                    score = self.minimax(self.board, False)
                    self.board[row][col] = None
                    if score > best_score:
                        best_score = score
                        best_move = (row, col)

        if best_move:
            self.make_move(best_move[0], best_move[1], "O")

        winner = self.check_winner()
        if winner:
            self.process_winner(winner)
            return

        if self.is_draw():
            QTimer.singleShot(2000, self.reset_board)
            return

        self.current_player = "X"

    def minimax(self, board, is_maximizing):
        winner = self.check_winner()
        if winner == "O": return 1
        if winner == "X": return -1
        if self.is_draw(): return 0

        if is_maximizing:
            best = -float('inf')
            for r in range(3):
                for c in range(3):
                    if board[r][c] is None:
                        board[r][c] = "O"
                        score = self.minimax(board, False)
                        board[r][c] = None
                        best = max(score, best)
            return best
        else:
            best = float('inf')
            for r in range(3):
                for c in range(3):
                    if board[r][c] is None:
                        board[r][c] = "X"
                        score = self.minimax(board, True)
                        board[r][c] = None
                        best = min(score, best)
            return best

    def make_move(self, row, col, player):
        self.board[row][col] = player
        btn = self.buttons[(row, col)]
        icon_path = f"assets/{player}_icon.png"
        btn.setIcon(QIcon(icon_path))
        btn.setIconSize(QSize(120, 120))
        if self.click_sound.isLoaded():
            self.click_sound.play()
            self.click_sound.setVolume(2)

    def process_winner(self, winner):
        if winner == "X":
            self.scores["ME"] += 1
            self.show_lose_avatar()
        else:
            self.scores["Æ"] += 1
            self.show_win_avatar()
        self.update_score_label()
        QTimer.singleShot(2000, self.reset_board)

    def is_draw(self):
        return all(cell is not None for row in self.board for cell in row)

    def show_preview(self, row, col):
        if self.board[row][col] is not None:
            return
        if self.current_player != "X":
            return
        icon_path = "assets/X_icon.png"
        btn = self.buttons[(row, col)]
        btn.setIcon(QIcon(icon_path))
        btn.setIconSize(QSize(60, 60))

    def clear_preview(self, row, col):
        if self.board[row][col] is not None:
            return
        self.buttons[(row, col)].setIcon(QIcon())

    def update_score_label(self):
        self.score_label.setText(f"ME: {self.scores['ME']}  vs  Æ: {self.scores['Æ']}")

    def reset_board(self):
        self.board = [[None for _ in range(3)] for _ in range(3)]
        self.current_player = "X"
        for btn in self.buttons.values():
            btn.setIcon(QIcon())

    def show_win_avatar(self):
        self.avatar.set_avatar("assets/aether_win.png")
        QTimer.singleShot(3000, lambda: self.avatar.set_avatar("assets/aether_idle.png"))

    def show_lose_avatar(self):
        self.avatar.set_avatar("assets/aether_lose.png")
        QTimer.singleShot(3000, lambda: self.avatar.set_avatar("assets/aether_idle.png"))

    def check_winner(self):
        for i in range(3):
            if self.board[i][0] == self.board[i][1] == self.board[i][2] and self.board[i][0]:
                return self.board[i][0]
            if self.board[0][i] == self.board[1][i] == self.board[2][i] and self.board[0][i]:
                return self.board[0][i]
        if self.board[0][0] == self.board[1][1] == self.board[2][2] and self.board[0][0]:
            return self.board[0][0]
        if self.board[0][2] == self.board[1][1] == self.board[2][0] and self.board[0][2]:
            return self.board[0][2]
        return None
