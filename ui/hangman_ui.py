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
    # Errors that the user can have 
    # based on the created art 
    HANGMAN_ART_ATTENDS = 8

    def __init__(self, gameModel = None):
        super().__init__()
        self.setWindowTitle(gameModel.get_name())
        self._model = gameModel
        self._rount = 0
        self._word2catch = ""
        self._round = 0
        pixmap_icon = qtg.QPixmap(":main_window/icon/bear_win_icon.png")
        self.setWindowIcon(qtg.QIcon(pixmap_icon))
        self._init_hangman_art = qtg.QPixmap(":hangman_art/illustration/hman_step_0.png")

        self._init_game_param()

        main_layout = qtw.QVBoxLayout()
        self.setLayout(main_layout)


        self._main_label2draw = qtw.QLabel()
        self._main_label2draw.setPixmap(self._init_hangman_art)
        main_layout.addWidget(self._main_label2draw)

        self._letter_layout = qtw.QHBoxLayout()
        main_layout.addLayout(self._letter_layout)
        # Set spaces for the user to fulfill 
        for _ in range(len(self._word2catch)):
            _tmp_e_line = qtw.QLineEdit()
            _tmp_e_line.textChanged.connect(self._next_move)
            self._letter_layout.addWidget(_tmp_e_line)

        _layout_buttons = qtw.QHBoxLayout()
        main_layout.addLayout(_layout_buttons)
        restart_button = qtw.QPushButton("Restart")
        end_button = qtw.QPushButton("Close")
        self._attends = qtw.QLabel("Attempts: %s" %("*"*self.HANGMAN_ART_ATTENDS))
        _layout_buttons.addWidget(self._attends)
        _layout_buttons.addWidget(restart_button)
        _layout_buttons.addWidget(end_button)

        self.show()

    def _init_game_param(self) -> None:
        self._model.start()
        self._word2catch = self._model.get_word2catch()

    def _next_move(self, text):
        letter = text

if __name__ == "__main__":
    app = qtw.QApplication(sys.argv)

    hman = Hangman_ui()

    sys.exit(app.exec())