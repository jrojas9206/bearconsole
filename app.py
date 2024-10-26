import sys
from PyQt5 import QtWidgets as qtw
from bearconsole.ui.hangman_ui import Hangman_ui
from bearconsole.ui.tictactoe_ui import Tictactoe_ui
from bearconsole.ui.game_console_ui import GameConsole
from bearconsole.games.tictactoe import TicTacToe
from bearconsole.games.hangman import Hangman

if __name__ == "__main__":
    app = qtw.QApplication(sys.argv)

    ttt_model = TicTacToe()
    ttt_ui = Tictactoe_ui(ttt_model)
    hm = Hangman()
    Hm_ui = Hangman_ui(hm)

    gamesDict = {"paperGames":[ttt_ui, Hm_ui], "mobileGames":[]}

    mw = GameConsole(gamesDict)

    sys.exit(app.exec())