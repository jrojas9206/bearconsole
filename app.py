import os 
import sys
from PyQt5 import QtWidgets as qtw
from PyQt5 import QtGui as qtg
from PyQt5 import QtCore as qtc
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget

from ui.tictactoe_ui import Tictactoe_ui
from ui.hangman_ui import Hangman_ui

from games.tictactoe import TicTacToe
from games.hangman import Hangman
from ui.game_console_ui import GameConsole

if __name__ == "__main__":
    app = qtw.QApplication(sys.argv)

    #ttt_model = TicTacToe()
    #mw = Tictactoe_ui(ttt_model)
    
    #hm = Hangman()
    #Hm_ui = Hangman_ui(hm)

    mw = GameConsole()

    sys.exit(app.exec())