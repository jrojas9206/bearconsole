from PyQt5 import QtWidgets as qtw
from PyQt5 import QtGui as qtg
from PyQt5 import QtCore as qtc
from bearconsole.resources import resources

class Hm_qeditline(qtw.QLabel):
    
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
    QLABEL_FONT_SIZE = 32
    QPUSHBUTTON_FONT_SIZE = 32
    QLINEEDIT_FONT_SIZE = 32
    GAME_ICON_PIXMAP = ":paper_games_icon/icon/hangman_icon.jpg"

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

        _layout_buttons = qtw.QHBoxLayout()
        main_layout.addLayout(_layout_buttons)
        restart_button = qtw.QPushButton("Restart")
        restart_button.setStyleSheet("font-size: %spx" %(self.QPUSHBUTTON_FONT_SIZE))
        restart_button.clicked.connect(self._restart)
        end_button = qtw.QPushButton("Close")
        end_button.setStyleSheet("font-size: %spx;" %(self.QPUSHBUTTON_FONT_SIZE))
        end_button.clicked.connect(self._close_widget)
        
        self._attends = qtw.QLabel("Attempts: %s" %("*"*self.HANGMAN_ART_ATTENDS))
        self._attends.setStyleSheet("font-size: %spx;" %(self.QLABEL_FONT_SIZE))
        self._qlable_used_letters = qtw.QLabel("Used Letters: []")
        self._qlable_used_letters.setStyleSheet("font-size: %spx; background-color: white;" %(self.QLABEL_FONT_SIZE))
        self.ql_input = qtw.QLabel("Input: ")
        self.ql_input.setStyleSheet("background-color: white; font-size: %spx" %(self.QLABEL_FONT_SIZE))
        self.input_character = qtw.QLineEdit()
        self.input_character.setMaxLength(self.MAX_LEN_CHARACTER_LINE_EDIT)
        self.input_character.setStyleSheet("font-size: %spx" %(self.QLINEEDIT_FONT_SIZE))
        self.input_character.textChanged.connect(self._next_move)

        _layout_buttons.addWidget(self._attends)
        _layout_buttons.addWidget(self._qlable_used_letters)
        _layout_buttons.addWidget(self.ql_input)
        _layout_buttons.addWidget(self.input_character)
        _layout_buttons.addWidget(restart_button)
        _layout_buttons.addWidget(end_button)

    def _close_widget(self):
        self.close()

    def _restart(self):
        self._main_label2draw.setPixmap(self._init_hangman_art)
        self._model.restart()
        self._init_game_param()
        self.dict_status = self._model.get_gamestatus()
        self.clearLayout(self._letter_layout)
        self.fill_layout(self._letter_layout, self._word2catch)
        self._qlable_used_letters.setText("Used Letters: ")
        self._attends.setText("Attempts: %s" %("*"*self.dict_status["lifes"]))

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
        else:
            if(text != ""):
                self._model.next_move(text)
                self.dict_status = self._model.get_gamestatus()
                update_art = qtg.QPixmap(":hangman_art/illustration/hman_step_%s.png" %(self.dict_status["art_id"]))
                self._main_label2draw.setPixmap(update_art)
                self._attends.setText("Attempts: %s" %("*"*self.dict_status["lifes"]))
        self._qlable_used_letters.setText("Used Letters: %s" %(str(self._model.get_used_letters())))
        self.input_character.clear()
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
            _tmp_e_line.setStyleSheet("background-color: white; font-size: %spx;" %(self.QLABEL_FONT_SIZE))
            #_tmp_e_line.setMaxLength(self.MAX_LEN_CHARACTER_LINE_EDIT)
            #_tmp_e_line.textChanged.connect(self._next_move)
            layout.addWidget(_tmp_e_line)

    def ui_verification(self):
        if self.dict_status:
            if self.dict_status['allLose'] or self.dict_status['lifes']==0:
                qtw.QMessageBox.warning(self,"Hangman", "You have lost!! Try again!")
                self._main_label2draw.setPixmap(self._init_hangman_art)
                self._model.restart()
                self._init_game_param()
                self._restart()
            if self.dict_status['winner'] != 0:
                qtw.QMessageBox.warning(self,"Hangman","You have won!!! Congratulations!!")
                self._main_label2draw.setPixmap(self._init_hangman_art)
                self._model.restart()
                self._init_game_param()
                self._restart()

    def show_game(self):
        self.show()

    def get_game_icon(self):
        return qtg.QIcon(qtg.QPixmap(self.GAME_ICON_PIXMAP))