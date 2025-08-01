from PyQt6.QtWidgets import QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout
from PyQt6.QtGui import QPixmap, QIcon, QFont, QCursor
from PyQt6.QtCore import Qt, QSize, QTimer, QThread, pyqtSignal
import random, os, time

CARD_PATH = "assets/cards/"
CARD_BACK = "back.png"
SUITS = ['H', 'D', 'S', 'C']
RANKS = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']

class DealerThread(QThread):
    update_gui = pyqtSignal()
    finished = pyqtSignal()

    def __init__(self, parent):
        super().__init__()
        self.parent = parent

    def run(self):
        while self.parent.calculate_hand_value(self.parent.dealer_hand) < 17:
            self.parent.dealer_hand.append(self.parent.deal_card())
            self.update_gui.emit()
            time.sleep(0.7)
        self.finished.emit()

class BlackjackGame(QWidget):
    def __init__(self, send_comment_callback=None):
        super().__init__()
        self.setWindowTitle("Blackjack with Aether Æ")
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setFixedSize(1000, 700)

        self.send_comment_callback = send_comment_callback
        self.deck = self.create_deck()
        self.balance = 1000
        self.bet = 100
        self.hands = [[]]
        self.active_hand_index = 0
        self.dealer_hand = []
        self.dealer_card_labels = []
        self.player_card_labels = []

        self.init_ui()
        self.new_round()

    def render_cards(self):
        if not self.hands or self.active_hand_index >= len(self.hands):
            return
        
        for lbl in self.dealer_card_labels + self.player_card_labels:
            lbl.deleteLater()
        self.dealer_card_labels.clear()
        self.player_card_labels.clear()

        reveal_all = self.active_hand_index >= len(self.hands)

        for i, card in enumerate(self.dealer_hand):
            label = QLabel(self.bg_label)
            if i == 1 and not reveal_all:
                pixmap = QPixmap(os.path.join(CARD_PATH, CARD_BACK))
            else:
                pixmap = QPixmap(os.path.join(CARD_PATH, f"{card}.png"))
            label.setPixmap(pixmap.scaled(80, 120, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))
            label.setGeometry(350 + i * 90, 100, 80, 120)
            label.show()
            self.dealer_card_labels.append(label)

        player_hand = self.hands[self.active_hand_index]
        for i, card in enumerate(player_hand):
            label = QLabel(self.bg_label)
            pixmap = QPixmap(os.path.join(CARD_PATH, f"{card}.png"))
            label.setPixmap(pixmap.scaled(80, 120, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))
            label.setGeometry(350 + i * 90, 420, 80, 120)
            label.show()
            self.player_card_labels.append(label)

    def init_ui(self):
        self.bg_label = QLabel(self)
        table = QPixmap("assets/blackjack.png")
        self.bg_label.setPixmap(table)
        self.bg_label.setGeometry(0, 0, self.width(), self.height())
        self.bg_label.setScaledContents(True)

        self.player_score = QLabel("0", self)
        self.player_score.setGeometry(450, 260, 100, 40)
        self.player_score.setStyleSheet("color: white;")
        self.player_score.setFont(QFont("FiraCode Nerd Font", 18, QFont.Weight.Bold))
        self.player_score.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.credit_label = QLabel(f"{self.balance}", self)
        self.credit_label.setGeometry(150, 260, 100, 40)
        self.credit_label.setStyleSheet("color: gold;")
        self.credit_label.setFont(QFont("FiraCode Nerd Font", 18, QFont.Weight.Bold))
        self.credit_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.button_box = QHBoxLayout()
        self.button_box.setSpacing(20)
        self.button_box.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.hit_button = self.make_button("Hit", self.hit)
        self.double_button = self.make_button("Double", self.double_down)
        self.stand_button = self.make_button("Stand", self.stand)
        self.split_button = self.make_button("Split", self.split_hand)

        container = QWidget(self)
        container.setGeometry(250, 610, 500, 50)
        container.setLayout(self.button_box)

        self.quit_button = self.make_button("Quit", self.close_game)
        self.quit_button.setParent(self)
        self.quit_button.setGeometry(900, 620, 80, 40)

    def make_button(self, label, callback):
        btn = QPushButton(label)
        btn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        btn.setFixedSize(100, 40)
        btn.setStyleSheet("""
            QPushButton {
                background-color: rgba(30, 0, 60, 0.8);
                color: #d9aaff;
                border: 2px solid #b478ff;
                border-radius: 12px;
                font: bold 14px "FiraCode Nerd Font";
            }
            QPushButton:hover {
                background-color: rgba(60, 0, 90, 0.9);
                border: 2px solid #e6ccff;
                color: white;
            }
        """)
        btn.clicked.connect(callback)
        self.button_box.addWidget(btn)
        return btn

    def create_deck(self):
        deck = [r + s for r in RANKS for s in SUITS]
        random.shuffle(deck)
        return deck

    def deal_card(self):
        if not self.deck:
            self.deck = self.create_deck()
        return self.deck.pop()

    def new_round(self):
        self.hands = [[self.deal_card(), self.deal_card()]]
        self.dealer_hand = [self.deal_card(), self.deal_card()]
        self.active_hand_index = 0
        self.update_ui()

        self.split_button.setEnabled(len(self.hands[0]) == 2 and self.get_card_value(self.hands[0][0]) == self.get_card_value(self.hands[0][1]))

    def hit(self):
        hand = self.hands[self.active_hand_index]
        hand.append(self.deal_card())
        self.update_ui()
        if self.calculate_hand_value(hand) > 21:
            self.next_hand_or_dealer()

    def double_down(self):
        hand = self.hands[self.active_hand_index]
        if len(hand) == 2:
            self.balance -= self.bet
            hand.append(self.deal_card())
            self.update_ui()
            self.next_hand_or_dealer()

    def stand(self):
        self.next_hand_or_dealer()

    def split_hand(self):
        if len(self.hands) == 1 and self.get_card_value(self.hands[0][0]) == self.get_card_value(self.hands[0][1]):
            self.balance -= self.bet
            card1 = self.hands[0][0]
            card2 = self.hands[0][1]
            self.hands = [[card1, self.deal_card()], [card2, self.deal_card()]]
            self.update_ui()
            self.split_button.setEnabled(False)
            if self.send_comment_callback:
                self.send_comment_callback("Æ: Splitting, are we? Twice the loss potential~")

    def next_hand_or_dealer(self):
        self.active_hand_index += 1
        if self.active_hand_index >= len(self.hands):
            self.dealer_thread = DealerThread(self)
            self.dealer_thread.update_gui.connect(self.render_cards)
            self.dealer_thread.finished.connect(self.resolve_round)
            self.dealer_thread.start()
        else:
            self.update_ui()

    def resolve_round(self):
        dealer_score = self.calculate_hand_value(self.dealer_hand)
        results = []
        for hand in self.hands:
            player_score = self.calculate_hand_value(hand)
            if player_score > 21:
                result = "lose"
            elif dealer_score > 21 or player_score > dealer_score:
                result = "win"
                self.balance += self.bet
            elif player_score == dealer_score:
                result = "push"
            else:
                result = "lose"
            results.append(result)

        if self.send_comment_callback:
            self.send_comment_callback(f"Æ: Results — {results}. Dealer had {dealer_score}.")
        self.credit_label.setText(str(self.balance))
        QTimer.singleShot(3000, self.new_round)

    def calculate_hand_value(self, hand):
        total = 0
        aces = 0
        for card in hand:
            rank = card[:-1]
            if rank in ['J', 'Q', 'K']:
                total += 10
            elif rank == 'A':
                aces += 1
                total += 11
            else:
                total += int(rank)
        while total > 21 and aces:
            total -= 10
            aces -= 1
        return total

    def get_card_value(self, card):
        return card[:-1]

    def update_ui(self):
        if not self.hands or self.active_hand_index >= len(self.hands):
            return
        
        hand = self.hands[self.active_hand_index]
        score = self.calculate_hand_value(hand)
        self.player_score.setText(str(score))
        self.credit_label.setText(str(self.balance))
        self.render_cards()

    def close_game(self):
        if self.send_comment_callback:
            self.send_comment_callback("Æ: Running away? Figures.")
        self.close()
