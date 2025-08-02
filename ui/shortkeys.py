from popup.confirm_blackjack import show_blackjack_dialog
from popup.confirm_ttt import show_ttt_dialog
from popup.confirm_chess import show_chess_dialog
from popup.confirm_checkers import show_checkers_dialog 
from popup.confirm_reboot import show_reboot_dialog   
from games.blackjack import BlackjackGame
from games.tictactoe import TicTacToeGame
from games.chess import ChessGame
from games.checkers import CheckersGame


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
    
    
    @staticmethod
    def handle_system_settings(chat_window, text):
        if text == "/reboot":
            if show_reboot_dialog(chat_window):
                chat_window.clear_conversation()
                chat_window.render_aether_response("*system has been reset successfully*")
            else:
                chat_window.render_aether_response("*no system changes has been made*")
            return True
        
    @staticmethod
    def handle_interactions(chat_window, text):
        prompts = {
            "/pinch": "The user has just pinched you.",
            "/tap": "The user is friendly tapping your shoulder.",
            "/pet": "The user is gently petting your head.",
            "/hug": "The user is giving you a friendly hug.",
            "/handshake": "The user gives you a handshake.",
            "/highfive": "The user gives you a high five.",
            "/facepalm": "The user is facepalming.",
        }

        if text in prompts:
            response = chat_window.ai.generate_response(prompts[text])
            chat_window.display_message("Æ", response)
            
        

            



        
        

        return False
