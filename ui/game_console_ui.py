import sys
from PyQt5 import QtWidgets as qtw
from PyQt5 import QtGui as qtg
from PyQt5 import QtCore as qtc
from bearconsole.resources import resources

class GamePushButton(qtw.QPushButton):
    def __init__(self):
        super().__init__()
        self.setMinimumSize(100, 100)
        self._id_button = 0

    def set_id_button(self, i_id:int) -> None:
        self._id_button = i_id

    def get_id_button(self) -> int:
        return self._id_button

class GameConsole(qtw.QMainWindow):

    MAIN_WINDOW_HEIGHT = 480
    MAIN_WINDOW_WIDTH = 720
    BACKGROUND_IMG = ":main_window/console/bear_main_logo.png"
    WINDOW_LOGO = ":main_window/icon/bear_win_icon.png"
    QLABEL_TITLE_FONT = qtg.QFont("Helvetica [Cronyx]", 21)
    GAME_LOGO_PUSHBUTTON = ":main_window/console/game_logo.png"

    def __init__(self, gamesDict:dict={}):
        super().__init__()
        self._games2load = gamesDict
        self.isPaper = False
        self.isMobile = False
        self._active_game_option = []
        self._group_game_option_idx = 0
        self._group_game_option_dict = {}
        self.setFixedSize(self.MAIN_WINDOW_WIDTH, self.MAIN_WINDOW_HEIGHT)
        self.setWindowTitle("Bear station")
        self.set_background_image(self.BACKGROUND_IMG)
        self.set_window_icon()
        self._qlabel_console_game = qtw.QLabel("Bear Station")
        self._qlabel_console_game.setFont(self.QLABEL_TITLE_FONT)
        self._paper_button_status = False
        self._mobile_button_status = False
        central_widget = qtw.QWidget()
        self.setCentralWidget(central_widget)
        mw_layout = qtw.QGridLayout(central_widget)

        self._qpush_button_paper = qtw.QPushButton("Paper games!")
        self._qpush_button_paper.setStyleSheet("background-color: balck; color: white; font-size: 22px;")
        self._qpush_button_paper.clicked.connect(self.paper_games)

        self._qpush_button_phone = qtw.QPushButton("Mobile games!")
        self._qpush_button_phone.setStyleSheet("background-color: balck; color: white; font-size: 22px;")
        self._qpush_button_phone.clicked.connect(self.mobile_games)

        self._init_gamebutton_icon_pixmap = qtg.QPixmap(self.GAME_LOGO_PUSHBUTTON)

        self._layout_games_pushbutton = qtw.QHBoxLayout()

        self._game_0 = GamePushButton()
        self._game_0.set_id_button(0)
        self._game_0.setIcon(qtg.QIcon(self._init_gamebutton_icon_pixmap))
        self._game_0.setIconSize(qtc.QSize(100, 100))
        self._game_0.clicked.connect(self.launch_game)

        self._game_1 = GamePushButton()
        self._game_1.set_id_button(1)
        self._game_1.setIcon(qtg.QIcon(self._init_gamebutton_icon_pixmap))
        self._game_1.setIconSize(qtc.QSize(100, 100))
        self._game_1.clicked.connect(self.launch_game)

        self._game_2 = GamePushButton()
        self._game_2.set_id_button(2)
        self._game_2.setIcon(qtg.QIcon(self._init_gamebutton_icon_pixmap))
        self._game_2.setIconSize(qtc.QSize(100, 100))
        self._game_2.clicked.connect(self.launch_game)

        mw_layout.addWidget(self._qlabel_console_game, 0, 0, qtc.Qt.AlignCenter | qtc.Qt.AlignTop)
        mw_layout.addWidget(self._qpush_button_paper, 0, 0, qtc.Qt.AlignLeft | qtc.Qt.AlignCenter)
        mw_layout.addWidget(self._qpush_button_phone, 0, 0, qtc.Qt.AlignRight | qtc.Qt.AlignCenter)

        mw_layout.addLayout(self._layout_games_pushbutton, 0, 0, qtc.Qt.AlignCenter | qtc.Qt.AlignBottom)

        self._layout_games_pushbutton.addWidget(self._game_0)
        self._layout_games_pushbutton.addWidget(self._game_1)
        self._layout_games_pushbutton.addWidget(self._game_2)
        self.show()

    def set_background_image(self, img_path):
        background_pixmap = qtg.QPixmap(img_path)
        background_pixmap.scaled(self.size(), qtc.Qt.IgnoreAspectRatio)
        mw_palette = qtg.QPalette()
        mw_palette.setBrush(mw_palette.Background, qtg.QBrush(background_pixmap))
        self.setPalette(mw_palette)

    def set_window_icon(self):
        icon = qtg.QPixmap(self.WINDOW_LOGO)
        self.setWindowIcon(qtg.QIcon(icon))

    def paper_games(self):
        self._qpush_button_phone.setStyleSheet("background-color: balck; color: white; font-size: 22px;")
        self._qpush_button_paper.setStyleSheet("background-color: gray; color: white; font-size: 22px;")
        self.isPaper = True
        self.isMobile = False
        self._related_game_to_launch_buttons("paperGames")
                

    def mobile_games(self):
        self.isPaper = False
        self.isMobile = True
        self._qpush_button_phone.setStyleSheet("background-color: gray; color: white; font-size: 22px;")
        self._qpush_button_paper.setStyleSheet("background-color: black; color: white; font-size: 22px;")
        self._related_game_to_launch_buttons("mobileGames")

    def _related_game_to_launch_buttons(self, gameRef:str):
        if(len(self._games2load[gameRef])>0 and 
           len(self._games2load[gameRef])<self._layout_games_pushbutton.count()):
            for idx, a_widget in enumerate(self._games2load[gameRef]):
                for a_button_id in range(self._layout_games_pushbutton.count()):
                    if idx == a_button_id:
                        widget =  self._layout_games_pushbutton.itemAt(a_button_id).widget()
                        widget.setIcon(a_widget.get_game_icon())
                        widget.setIconSize(qtc.QSize(100, 100))
                        break
        if len(self._games2load[gameRef])>self._layout_games_pushbutton.count(): # If the name of games is bigger that the available buttons what to do?
            pass
        elif len(self._games2load[gameRef])==0:
            for a_button_id in range(self._layout_games_pushbutton.count()):
                widget =  self._layout_games_pushbutton.itemAt(a_button_id).widget()
                widget.setIcon(qtg.QIcon(self._init_gamebutton_icon_pixmap))
                widget.setIconSize(qtc.QSize(100, 100))

    def launch_game(self):
        sender = self.sender()
        button_id = sender.get_id_button()

        if not self.isMobile and self.isPaper:
            games = self._games2load["paperGames"]
        elif self.isMobile and not self.isPaper:
            games = self._games2load["mobileGames"]
        elif not self.isMobile and not self.isPaper:
            games = []
        else:
            raise ValueError("Unknow option, verify menu configuration")
        
        if(button_id+1 <= len(games)):
            games[button_id].show_game()
        else:
            image_warning = qtg.QPixmap(":main_window/console/warning.jpg")
            messageBox = qtw.QMessageBox()
            messageBox.setIconPixmap(image_warning)
            messageBox.setText("No game available!")
            messageBox.setWindowTitle("Bear Station: Warning!")
            messageBox.setWindowIcon(qtg.QIcon(qtg.QPixmap(self.WINDOW_LOGO)))
            messageBox.exec()

if __name__ == '__main__':
    app = qtw.QApplication(sys.argv)
    mw = GameConsole()
    sys.exit(app.exec())
