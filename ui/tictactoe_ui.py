import os 
import sys
from PyQt5 import QtWidgets as qtw
from PyQt5 import QtGui as qtg
from PyQt5 import QtCore as qtc
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget
import resources

class PushButton_xo(qtw.QPushButton):
    def __init__(self):
        super().__init__()


class MainWindow(qtw.QWidget):

    def __init__(self):
        """MainWindow constructor.

        This widget will be our main window.
        We'll define all the UI components in here.
        """
        super().__init__()
        #self.setFixedSize(480, 480)
        board_layout = qtw.QGridLayout()
        self.setLayout(board_layout)
        for a_row in range(3):
            for a_column in range(3):
                button_xo = qtw.QPushButton(" ")
                button_xo.setMinimumWidth(100)
                button_xo.setMinimumHeight(100)
                board_layout.layout().addWidget(button_xo, a_row, a_column)
        self.show()

    

if __name__ == '__main__':
    app = qtw.QApplication(sys.argv)
    # it's required to save a reference to MainWindow.
    # if it goes out of scope, it will be destroyed.
    mw = MainWindow()
    sys.exit(app.exec())
