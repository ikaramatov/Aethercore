from ui.confirm_blackjack import show_blackjack_dialog
from ui.confirm_ttt import show_ttt_dialog
from ui.confirm_chess import show_chess_dialog
from games.blackjack import BlackjackGame
from games.tictactoe import TicTacToeGame
from games.chess import ChessGame
from games.checkers import CheckersGame
from ui.confirm_checkers import show_checkers_dialog    

class HandleShortkeys:
    @staticmethod
    def handle_games(chat_window, text):
        text = text.strip()

        if text == "/blackjack":
            if show_blackjack_dialog(chat_window):
                chat_window.blackjack_window = BlackjackGame(send_comment_callback=chat_window.render_aether_response)
                chat_window.blackjack_window.show()
            else:    
                chat_window.render_aether_response("...")
            return True
        
        elif text in ("/tictactoe", "/ttt"):
            if show_ttt_dialog(chat_window):
                chat_window.ttt_window = TicTacToeGame(send_comment_callback=chat_window.render_aether_response)
                chat_window.ttt_window.show()
            else:
                chat_window.render_aether_response("...")
            return True
        
        elif text == "/chess":
            if show_chess_dialog(chat_window):
                chat_window.chess_window = ChessGame(send_comment_callback=chat_window.render_aether_response)
                chat_window.chess_window.show()
            else:
                chat_window.render_aether_response("...")
            return True
        
        elif text == "/checkers":
            if show_checkers_dialog(chat_window):
                chat_window.checkers_window = CheckersGame(send_comment_callback=chat_window.render_aether_response)
                chat_window.checkers_window.show()
            else:
                chat_window.render_aether_response("Another time then...")
            return True

        
        

        return False
