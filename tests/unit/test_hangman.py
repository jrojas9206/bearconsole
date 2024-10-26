import sys 
from PyQt5 import QtWidgets as qtw
from bearconsole.ui.hangman_ui import Hangman_ui
from bearconsole.games.hangman import Hangman

if __name__ == "__main__":
    app = qtw.QApplication(sys.argv)
    gameObj = Hangman()
    # it's required to save a reference to MainWindow.
    # if it goes out of scope, it will be destroyed.
    mw = Hangman_ui(gameObj)
    mw.show_game()
    sys.exit(app.exec())