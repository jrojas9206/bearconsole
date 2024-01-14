import sys
import time
from PyQt5 import QtWidgets as qtw
from PyQt5 import QtGui as qtg
from PyQt5 import QtCore as qtc
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget
try:
    import resources
except ModuleNotFoundError:
    import ui.resources

class Hm_qeditline(qtw.QLineEdit):
    
    def __init__(self):
        super().__init__()
        self._id_pos = 0
    
    def set_id_pos(self, id:int) -> None:
        self._id_pos = id

    def get_id_pos(self) -> int:
        return self._id_pos

class Hangman_ui(qtw.QWidget):
    # Errors that the user can have 
    # based on the created art 
    HANGMAN_ART_ATTENDS = 7
    MAX_LEN_CHARACTER_LINE_EDIT = 1

    def __init__(self, gameModel = None):
        super().__init__()
        self.setWindowTitle(gameModel.get_name())
        self._model = gameModel
        self._rount = 0
        self._word2catch = ""
        self._round = 0
        self.dict_status = {}
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
        self.fill_layout(self._letter_layout, self._word2catch)
        # for idx in range(len(self._word2catch)):
        #     _tmp_e_line = Hm_qeditline()
        #     _tmp_e_line.set_id_pos(idx)
        #     _tmp_e_line.setMaxLength(self.MAX_LEN_CHARACTER_LINE_EDIT)
        #     _tmp_e_line.textChanged.connect(self._next_move)
        #     self._letter_layout.addWidget(_tmp_e_line)

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
        sender = self.sender()
        nWidget = self._letter_layout.count()
        lck = False

        if (text in self._word2catch and 
            text != " " and text != "" and text != "\r"):
            for idx, a_word in enumerate(self._word2catch):
                # Set the letter in the qlabel that the user edited
                self._model.next_move(text)
                for a_idx_widget in range(self._letter_layout.count()):
                    if a_idx_widget == idx and  a_word == text:
                        oWidget = self._letter_layout.itemAt(idx).widget()
                        oWidget.setText(text)
                        self.dict_status = self._model.get_gamestatus()
                        oWidget.setEnabled(False)
                        print(self.dict_status)  
        else:
            if(text != ""):
                self._model.next_move("\r")
                self.dict_status = self._model.get_gamestatus()
                update_art = qtg.QPixmap(":hangman_art/illustration/hman_step_%s.png" %(self.dict_status["art_id"]))
                self._main_label2draw.setPixmap(update_art)
                self._attends.setText("Attempts: %s" %("*"*self.dict_status["lifes"]))
        self.ui_verification()

    def clearLayout(self, layout):
        while layout.count():
            child = layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()    
    
    def fill_layout(self, layout, text):
        for idx in range(len(text)):
            _tmp_e_line = Hm_qeditline()
            _tmp_e_line.set_id_pos(idx)
            _tmp_e_line.setMaxLength(self.MAX_LEN_CHARACTER_LINE_EDIT)
            _tmp_e_line.textChanged.connect(self._next_move)
            layout.addWidget(_tmp_e_line)

    def ui_verification(self):
        if self.dict_status:
            if self.dict_status['allLose'] or self.dict_status['lifes']==0:
                print( self.dict_status['allLose'], self.dict_status['lifes'])
                qtw.QMessageBox.warning(self,"Hangman", "You have lost!! Try again!")
                self._main_label2draw.setPixmap(self._init_hangman_art)
                self._model.restart()
                self._init_game_param()
                self.dict_status = self._model.get_gamestatus()
                self.clearLayout(self._letter_layout)
                self.fill_layout(self._letter_layout, self._word2catch)
                self._attends.setText("Attempts: %s" %("*"*self.dict_status["lifes"]))
                
            if self.dict_status['winner'] != 0:
                qtw.QMessageBox.warning(self,"Hangman","You have won!!! Congratulations!!")
                self._main_label2draw.setPixmap(self._init_hangman_art)
                self._model.restart()
                self._init_game_param()
                self.dict_status = self._model.get_gamestatus()
                self.clearLayout(self._letter_layout)
                self.fill_layout(self._letter_layout, self._word2catch)
                self._attends.setText("Attempts: %s" %("*"*self.dict_status["lifes"]))