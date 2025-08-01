from PyQt6.QtGui import QTextCursor, QColor, QTextCharFormat
from PyQt6.QtWidgets import QTextEdit
from PyQt6.QtCore import QTimer

def append_colored_text(chat_area: QTextEdit, text: str, color: str = "white", newline: bool = True):
    cursor = chat_area.textCursor()
    cursor.movePosition(QTextCursor.MoveOperation.End)

    fmt = QTextCharFormat()
    fmt.setForeground(QColor(color))
    cursor.setCharFormat(fmt)
    
    if newline:
        cursor.insertText(text + "\n", fmt)
    else:
        cursor.insertText(text, fmt)

    chat_area.setTextCursor(cursor)
    chat_area.ensureCursorVisible()


def animate_typing(chat_area, text, color="white", chat_window=None):
    cursor = chat_area.textCursor()
    chat_area.moveCursor(QTextCursor.MoveOperation.End)
    
    fmt = QTextCharFormat()
    fmt.setForeground(QColor(color))
    cursor.setCharFormat(fmt)    

    idx = 0
    timer = QTimer()

    def type_char():
        nonlocal idx
        if chat_window and chat_window.stop_requested:
            timer.stop()
            chat_window.finish_generation()
            return
        
        if idx < len(text):
            cursor.insertText(text[idx], fmt)
            chat_area.setTextCursor(cursor)
            chat_area.ensureCursorVisible()
            idx += 1
        else:
            timer.stop()
            cursor.insertText("\n", fmt)
            chat_window.finish_generation() if chat_window else None

    timer.timeout.connect(type_char)
    timer.start(20)

    if chat_window:
        chat_window.current_animation_timer = timer
        chat_window.generating = True
        chat_window.stop_requested = False
        chat_window.stop_button.show()

