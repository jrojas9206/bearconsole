"""
Launch the terminal console game 

Date: 231230
Author: Juan Pablo ROJAS 
Requirements: PyQt5
"""
import sys 
from games.tictactoe import TicTacToe
from board.board_generic import Board
from menu.generic_menu import Menu

def test_winner_player2():
    ttt = TicTacToe()
    b = Board()
    
    b.load_game(ttt)

    player = {
        "playerID": 1,  # 0 or 1
        "playerSelection": [1,'A'] # coordinates [row:int, columns:str]
    }
    
    ttt.update(player)

    player = {
        "playerID": 1,  # 0 or 1
        "playerSelection": [2,'B'] # coordinates [row:int, columns:str]
    }
    
    ttt.update(player)

    player = {
        "playerID": 1,  # 0 or 1
        "playerSelection": [3,'C'] # coordinates [row:int, columns:str]
    }

    ttt.update(player)

    b.display_board()
    print("----")

def test_board():
    ttt = TicTacToe()
    b = Board()

    b.load_game(ttt)
    print(b.get_game_name())

    b.display_board()

    b.who_have_to_play()

    b.next_move(1, "B")
    b.display_board()

    b.who_have_to_play()

    b.next_move(2, "B")
    b.display_board()

    b.who_have_to_play()

def test_menu():
    ttt = TicTacToe()
    b = Board()
    m = Menu({0: ttt, 1:ttt}, b)
    m.start_menu()


def main():
    #test_winner_player2()
    #test_board()
    test_menu()

    return 0

if __name__ == "__main__":
    sys.exit(main())