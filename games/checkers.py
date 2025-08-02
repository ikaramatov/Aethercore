import sys
from copy import deepcopy
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QPushButton, QGridLayout
from PyQt6.QtGui import QFont, QColor, QPainter, QBrush, QPen
from PyQt6.QtCore import Qt, QTimer, pyqtSignal, QPoint


class CheckersGame(QWidget):
    game_over = pyqtSignal(str)

    def __init__(self, send_comment_callback=None):
        super().__init__()
        self.setWindowTitle("Checkers with Aether ⛃")

        self.send_comment_callback = send_comment_callback
        self.game_closed_callback = None

        self.board_size = 8
        self.square_size = 66  # 8 * 66 = 528, same as chess
        self.selected_piece = None
        self.valid_moves = []
        self.current_player = 'white'
        self.is_game_over = False
        self.board = self.create_starting_board()

        # Layout
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)

        # Status Label
        self.status_label = QLabel("White's move.")
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.status_label.setFont(QFont("Courier", 14))
        self.layout.addWidget(self.status_label)

        # Grid layout
        self.grid = QGridLayout()
        self.grid.setSpacing(0)
        self.grid.setContentsMargins(0, 0, 0, 0)
        self.squares = {}

        for row in range(self.board_size):
            for col in range(self.board_size):
                square = CheckerSquare(row, col)
                square.setFixedSize(self.square_size, self.square_size)
                square.square_clicked.connect(self.handle_square_click)
                self.grid.addWidget(square, row, col)
                self.squares[(row, col)] = square

        # Grid container
        self.grid_widget = QWidget()
        self.grid_widget.setLayout(self.grid)
        self.grid_widget.setFixedSize(528, 528)
        self.layout.addWidget(self.grid_widget, alignment=Qt.AlignmentFlag.AlignCenter)

        # Reset Button
        self.reset_button = QPushButton("Reset Game")
        self.reset_button.clicked.connect(self.reset_game)
        self.layout.addWidget(self.reset_button)

        self.setLayout(self.layout)
        self.setFixedSize(self.sizeHint())
        self.update_board()

    def init_ui(self):
        self.layout = QVBoxLayout()
        self.status_label = QLabel("White's turn")
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.status_label.setFont(QFont("Courier", 14))
        self.layout.addWidget(self.status_label)

        self.grid = QGridLayout()
        self.squares = {}
        for row in range(self.board_size):
            for col in range(self.board_size):
                square = CheckerSquare(row, col)
                square.setFixedSize(self.square_size, self.square_size)
                square.square_clicked.connect(self.handle_square_click)
                self.grid.addWidget(square, row, col)
                self.squares[(row, col)] = square

        board_widget = QWidget()
        board_widget.setLayout(self.grid)
        self.layout.addWidget(board_widget)

        self.reset_button = QPushButton("Reset Game")
        self.reset_button.clicked.connect(self.reset_game)
        self.layout.addWidget(self.reset_button)

        self.setLayout(self.layout)
        self.update_board()

    def create_starting_board(self):
        board = [[None for _ in range(self.board_size)] for _ in range(self.board_size)]
        for row in range(3):
            for col in range(self.board_size):
                if (row + col) % 2 == 1:
                    board[row][col] = {'color': 'black', 'king': False}
        for row in range(5, 8):
            for col in range(self.board_size):
                if (row + col) % 2 == 1:
                    board[row][col] = {'color': 'white', 'king': False}
        return board

    def update_board(self):
        for row in range(self.board_size):
            for col in range(self.board_size):
                piece = self.board[row][col]
                square = self.squares[(row, col)]
                square.set_default_style()
                square.set_piece(piece)
                if self.selected_piece == (row, col):
                    square.set_selected_style()
                elif (row, col) in self.valid_moves:
                    square.set_valid_move_style()

    def handle_square_click(self, row, col):
        if self.is_game_over:
            return
        piece = self.board[row][col]
        if self.selected_piece:
            if (row, col) in self.valid_moves:
                self.make_move(self.selected_piece, (row, col))
                self.selected_piece = None
                self.valid_moves = []
                self.switch_player()
            elif piece and piece['color'] == self.current_player:
                self.select_piece((row, col))
            else:
                self.selected_piece = None
                self.valid_moves = []
        elif piece and piece['color'] == self.current_player:
            self.select_piece((row, col))
        self.update_board()

    def select_piece(self, position):
        self.selected_piece = position
        self.valid_moves = self.get_valid_moves(position)
        if not self.valid_moves:
            self.selected_piece = None
            self.status_label.setText(f"No valid moves for this {self.current_player} piece")

    def get_valid_moves(self, position):
        row, col = position
        piece = self.board[row][col]
        if not piece:
            return []
        moves, captures = [], []
        directions = [(-1, -1), (-1, 1)] if piece['color'] == 'white' else [(1, -1), (1, 1)]
        if piece['king']:
            directions += [(-1, -1), (-1, 1), (1, -1), (1, 1)]
        for dr, dc in directions:
            nr, nc = row + dr, col + dc
            if 0 <= nr < self.board_size and 0 <= nc < self.board_size:
                target = self.board[nr][nc]
                if not target:
                    moves.append((nr, nc))
                elif target['color'] != piece['color']:
                    jr, jc = nr + dr, nc + dc
                    if 0 <= jr < self.board_size and 0 <= jc < self.board_size and not self.board[jr][jc]:
                        captures.append((jr, jc))
        return captures if captures else moves

    def make_move(self, start, end):
        sr, sc = start
        er, ec = end
        piece = self.board[sr][sc]
        self.board[er][ec] = piece
        self.board[sr][sc] = None
        if not piece['king'] and ((piece['color'] == 'white' and er == 0) or (piece['color'] == 'black' and er == 7)):
            piece['king'] = True
        if abs(sr - er) == 2:
            self.board[(sr + er) // 2][(sc + ec) // 2] = None
        if self.check_win_condition():
            self.is_game_over = True
            winner = self.current_player
            self.status_label.setText(f"Game Over! {winner.capitalize()} wins!")
            self.game_over.emit(winner)
        self.update_board()

    def check_win_condition(self):
        opponent = 'black' if self.current_player == 'white' else 'white'
        return not any(
            piece and piece['color'] == opponent and self.get_valid_moves((r, c))
            for r in range(self.board_size)
            for c, piece in enumerate(self.board[r])
        )

    def switch_player(self):
        self.current_player = 'black' if self.current_player == 'white' else 'white'
        self.status_label.setText(f"{self.current_player.capitalize()}'s turn")
        if self.current_player == 'black':
            QTimer.singleShot(500, self.ai_move)

    def ai_move(self):
        _, best_board = minimax(self.board, 3, True, 'black')
        if best_board:
            self.board = best_board
            self.update_board()
            if self.check_win_condition():
                self.is_game_over = True
                self.status_label.setText("Game Over! Black wins!")
                self.game_over.emit('black')
            else:
                self.switch_player()

    def reset_game(self):
        self.board = self.create_starting_board()
        self.current_player = 'white'
        self.selected_piece = None
        self.valid_moves = []
        self.is_game_over = False
        self.status_label.setText("White's turn")
        self.update_board()

    def closeEvent(self, event):
        if self.game_closed_callback:
            self.game_closed_callback()
        super().closeEvent(event)


def minimax(board, depth, max_player, color):
    opponent = 'black' if color == 'white' else 'white'
    winner = get_winner(board)
    if depth == 0 or winner:
        return evaluate_board(board, color), board

    if max_player:
        max_eval = float('-inf')
        best_board = None
        for new_board in get_all_moves(board, color):
            evaluation, _ = minimax(new_board, depth - 1, False, color)
            if evaluation > max_eval:
                max_eval = evaluation
                best_board = new_board
        return max_eval, best_board
    else:
        min_eval = float('inf')
        best_board = None
        for new_board in get_all_moves(board, opponent):
            evaluation, _ = minimax(new_board, depth - 1, True, color)
            if evaluation < min_eval:
                min_eval = evaluation
                best_board = new_board
        return min_eval, best_board


def get_all_moves(board, color):
    boards = []
    for r in range(8):
        for c in range(8):
            piece = board[r][c]
            if piece and piece['color'] == color:
                for move in get_valid_moves_for_sim(board, (r, c)):
                    temp_board = deepcopy(board)
                    make_simulated_move(temp_board, (r, c), move)
                    boards.append(temp_board)
    return boards


def get_valid_moves_for_sim(board, position):
    row, col = position
    piece = board[row][col]
    if not piece:
        return []
    directions = [(-1, -1), (-1, 1)] if piece['color'] == 'white' else [(1, -1), (1, 1)]
    if piece['king']:
        directions += [(-1, -1), (-1, 1), (1, -1), (1, 1)]
    moves, captures = [], []
    for dr, dc in directions:
        nr, nc = row + dr, col + dc
        if 0 <= nr < 8 and 0 <= nc < 8:
            target = board[nr][nc]
            if not target:
                moves.append((nr, nc))
            elif target['color'] != piece['color']:
                jr, jc = nr + dr, nc + dc
                if 0 <= jr < 8 and 0 <= jc < 8 and not board[jr][jc]:
                    captures.append((jr, jc))
    return captures if captures else moves


def make_simulated_move(board, start, end):
    sr, sc = start
    er, ec = end
    piece = board[sr][sc]
    board[er][ec] = piece
    board[sr][sc] = None
    if abs(sr - er) == 2:
        board[(sr + er) // 2][(sc + ec) // 2] = None
    if not piece['king'] and ((piece['color'] == 'white' and er == 0) or (piece['color'] == 'black' and er == 7)):
        piece['king'] = True


def get_winner(board):
    white, black = 0, 0
    for row in board:
        for piece in row:
            if piece:
                if piece['color'] == 'white':
                    white += 1
                else:
                    black += 1
    if white == 0:
        return 'black'
    elif black == 0:
        return 'white'
    return None


def evaluate_board(board, color):
    score = 0
    for row in board:
        for piece in row:
            if piece:
                value = 2 if piece['king'] else 1
                score += value if piece['color'] == color else -value
    return score


class CheckerSquare(QPushButton):
    square_clicked = pyqtSignal(int, int)

    def __init__(self, row, col):
        super().__init__()
        self.row = row
        self.col = col
        self.piece = None
        self.clicked.connect(lambda: self.square_clicked.emit(self.row, self.col))
        self.set_default_style()

    def set_piece(self, piece):
        self.piece = piece
        self.update()

    def set_default_style(self):
        color = "#f0d9b5" if (self.row + self.col) % 2 == 0 else "#b58863"
        self.setStyleSheet(f"background-color: {color}; border: none;")
        self.update()

    def set_selected_style(self):
        self.setStyleSheet("background-color: #b5c7f0; border: 2px solid #4a6ed9;")

    def set_valid_move_style(self):
        self.setStyleSheet("background-color: #c7f0b5; border: 2px solid #4ad96e;")

    def paintEvent(self, event):
        super().paintEvent(event)
        if not self.piece:
            return
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        color = QColor(255, 255, 255) if self.piece['color'] == 'white' else QColor(0, 0, 0)
        painter.setBrush(QBrush(color))
        painter.setPen(QPen(Qt.GlobalColor.black, 2))
        center = self.rect().center()
        radius = min(self.width(), self.height()) // 2 - 10
        painter.drawEllipse(center, radius, radius)
        if self.piece['king']:
            painter.setBrush(QBrush(QColor(255, 215, 0)))
            painter.setPen(QPen(Qt.GlobalColor.black, 1))
            points = [
                center + QPoint(-radius//2, -radius//3),
                center + QPoint(0, -radius//2),
                center + QPoint(radius//2, -radius//3),
                center + QPoint(radius//4, 0),
                center + QPoint(0, radius//6),
                center + QPoint(-radius//4, 0)
            ]
            painter.drawPolygon(points)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    game = CheckersGame()
    game.show()
    sys.exit(app.exec())
