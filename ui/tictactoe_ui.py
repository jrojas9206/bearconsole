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

class PushButton_xo(qtw.QPushButton):
    def __init__(self):
        super().__init__()
        self._user = "crosss" 
        self._row = -1
        self._col = ""
        self._ref_col = ["A", "B", "C"]
    
    def on_click(self):
        print("ok")
        if self._user == "cross":
            i_icon = qtg.QPixmap(':players_icon/icon/delete.png')
        elif self._user == "circle":
            i_icon = qtg.QPixmap(':players_icon/icon/circle.png')
        else:
            raise ValueError("Unexpected user IDname")
        self.setIcon(qtg.QIcon(i_icon))

    def update_user(self):
        self._user = "circle"

    def set_row(self, a_row:int):
        self._row = a_row

    def set_col(self, a_column:str):
        if a_column not in self._ref_col:
            raise ValueError("Unexpected column name %s" %(a_column))
        self._col = a_column

    def get_row(self):
        return self._row
    
    def get_column(self):
        return self._col

class Tictactoe_ui(qtw.QWidget):

    def __init__(self, gameModel=None):
        """MainWindow constructor.

        This widget will be our main window.
        We'll define all the UI components in here.
        """
        super().__init__()
        self._model = gameModel
        self._round = 0
        ref_dic = {
            0: "A",
            1: "B",
            2: "C",
        }
        # Start game model
        self._model.start()
        #self.setFixedSize(480, 480)
        board_layout = qtw.QGridLayout()
        self.setLayout(board_layout)
        for a_row in range(3):
            for a_column in range(3):
                button_xo = PushButton_xo()
                button_xo.set_row(a_row+1)
                button_xo.set_col(ref_dic[a_column])
                button_xo.clicked.connect(self.on_click)
                button_xo.setMinimumWidth(100)
                button_xo.setMinimumHeight(100)
                board_layout.layout().addWidget(button_xo, a_row, a_column)

        self.show()

    def on_click(self):
        sender = self.sender()
        if self._model is None:
            if self._round%2 == 0:
                i_icon = qtg.QPixmap(":players_icon/icon/delete.png")
            else:
                i_icon = qtg.QPixmap(":players_icon/icon/circle.png")
            sender.setIcon(qtg.QIcon(i_icon))
            self._round += 1
        else:
            a_row = sender.get_row()
            a_column = sender.get_column()
            try:
                self._model.next_move(a_row, a_column)
            except Warning as warn:
                qtw.QMessageBox.warning(self, "Tictactoe", "Select another position. This one is already taken!")
            if self._model.get_player() == 0:
                i_icon = qtg.QPixmap(":players_icon/icon/delete.png")
            else:
                i_icon = qtg.QPixmap(":players_icon/icon/circle.png")
            sender.setIcon(qtg.QIcon(i_icon))
            status_dict = self._model.get_gamestatus() 
            if status_dict["winner"] != 0:
                qtw.QMessageBox.warning(self, "Tictactoe", "Player %s you have win the game!! Congratulations!!" %(status_dict["winner"])) 
                self.close()
            if status_dict["winner"] == 0 and status_dict["end"]:
                qtw.QMessageBox.warning(self, "Tictactoe", "There is no winners this time! play again!!") 
                self.close()

if __name__ == '__main__':
    app = qtw.QApplication(sys.argv)
    # it's required to save a reference to MainWindow.
    # if it goes out of scope, it will be destroyed.
    mw = Tictactoe_ui()
    sys.exit(app.exec())
