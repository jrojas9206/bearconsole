"""
Generic terminal board 
The model creates a string that represent 
the board of the game and displayed

Date: 231230
Author: Juan Pablo ROJAS 
Requirements: PyQt5
"""
import sys 

class Board:
    """
        Class to visualize in the terminal  
        the different games    
    """
    def __init__(self):
        self._game_board_ = None
        self._board = ""
        self._igame = ""

    def load_game(self, game):
        """
            Load the game object

            :param game: Game object, Object with the logic of the game
        """
        self._igame = game
        self._igame.start()
        self._get_board()

    def _get_board(self) -> None:
        self._game_board_ = self._igame.get_board()

    def get_game_name(self):
        return self._igame.get_name() 

    def prepare_board(self):
        """
            Print the board in its actual state 
        """
        a_board = ""
        for a_row in self._game_board_:
            a_board += "".join(a_row+["\n"])
        self._board_view = a_board

    def who_have_to_play(self):
        """
            Print the player that the to move 
        """
        display_player = """############################
It is your turn player: %s
############################
                          """ %(self._igame.get_player()+1)
        print(display_player)

    def get_who_plays_id(self):
        """
            Get the ID of the player who have to play 
            :return: int, 
        """
        return self._igame.get_player() 
    
    def next_move(self, row:int, column:str):
        """
            Execute a move action for the actual round 
            :param row: int, Row in the board
            :param column: str, Column name [A-Z]             
        """
        try:
            self._igame.next_move(row, column)
        except Warning as w:
            print(w)

    def display_board(self):
        status_msg = """##########################
# ROUND: %s               #
# Your turn player: %s    #
##########################
""" %(self._igame.get_actual_round_id(), 
      self._igame.get_player()+1)
        self.prepare_board()
        print(self._board_view)
        print(status_msg)