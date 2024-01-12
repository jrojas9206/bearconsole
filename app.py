import os 
import sys
from PyQt5 import QtWidgets as qtw
from PyQt5 import QtGui as qtg
from PyQt5 import QtCore as qtc
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget

from ui.tictactoe_ui import Tictactoe_ui
from games.tictactoe import TicTacToe




if __name__ == "__main__":
    app = qtw.QApplication(sys.argv)

    ttt_model = TicTacToe()

    mw = Tictactoe_ui(ttt_model)
    
    sys.exit(app.exec())