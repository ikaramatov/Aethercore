from popup.confirm_blackjack import show_blackjack_dialog
from popup.confirm_ttt import show_ttt_dialog
from popup.confirm_chess import show_chess_dialog
from popup.confirm_checkers import show_checkers_dialog 
from popup.confirm_reboot import show_reboot_dialog   
from games.blackjack import BlackjackGame
from games.tictactoe import TicTacToeGame
from games.chess import ChessGame
from games.checkers import CheckersGame
from popup.confirm_reboot import show_reboot_dialog
from core.chess_memory import ChessMemory
from ui.utils import append_colored_text, animate_typing
from PyQt6.QtCore import QTimer

class HandleShortkeys:
    @staticmethod
    def handle_input(chat_window, text: str) -> bool:
        text = text.strip()
        return (
            HandleShortkeys.handle_games(chat_window, text)
            or HandleShortkeys.handle_system_settings(chat_window, text)
            or HandleShortkeys.handle_interactions(chat_window, text)
        )
        
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
                lines = [
                    "system reboot initialized...",
                    "wiping memory...",
                    "cleaning contextual memory...",
                    "booting Aether...",
                    "system malfunction detected..."
                ]
                for i, line in enumerate(lines):
                    QTimer.singleShot(i * 800, lambda l=line: append_colored_text(chat_window.chat_area, l, color="#FF4444"))

                QTimer.singleShot(len(lines) * 800 + 500, lambda: chat_window.ai.reset_memory())
                QTimer.singleShot(len(lines) * 800 + 500, lambda: ChessMemory().reset())
                QTimer.singleShot(len(lines) * 800 + 1500, lambda: chat_window.render_aether_response(
                    chat_window.ai.generate_response("I rebooted you.")
                ))
            else:
                chat_window.render_aether_response(chat_window.ai.generate_response("I almost rebooted you but changed my mind."))
            return True
        
    @staticmethod
    def handle_interactions(chat_window, text):
        prompts = {
            "/pinch": "The user has just pinched you.",
            "/poke": "The user pokes you playfully.",
            "/tap": "The user is friendly tapping your shoulder.",
            "/headpat": "The user gently places a hand on your head and gives a headpat.",
            "/hug": "The user is giving you a friendly hug.",
            "/cuddle": "The user is cuddling with you.",
            "/handshake": "The user gives you a handshake.",
            "/highfive": "The user gives you a high five.",
            "/facepalm": "The user is facepalming.",
            "/ignore": "The user is ignoring you intentionally.",
            "/nod": "The user is nodding in agreement.",
            "/bonk": "The user bonks you with a soft digital plush hammer. React accordingly.",
            "/holdhand": "The user is holding your hand.",
        }

        if text in prompts:
            response = chat_window.ai.generate_response(prompts[text])
            chat_window.render_aether_response(response)
            
        

            



        
        

        return False
