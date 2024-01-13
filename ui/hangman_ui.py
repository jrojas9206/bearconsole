import sys
from PyQt5 import QtWidgets as qtw
from PyQt5 import QtGui as qtg
from PyQt5 import QtCore as qtc
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget
try:
    import resources
except ModuleNotFoundError:
    import ui.resources

class Hangman_ui(qtw.QWidget):

    def __init__(self, gameModel = None):
        super().__init__()

        self.show()

if __name__ == "__main__":
    app = qtw.QApplication(sys.argv)

    hman = Hangman_ui()

    sys.exit(app.exec())