"""
HangMan
Model-View implementation 

Date: 231230
Author: Juan Pablo ROJAS 
Requirements: PyQt5
"""
from random import randrange
try:
    from extras import hangman_art
    from extras import hangman_dictionary
except ModuleNotFoundError:
    from games.extras import hangman_art
    from games.extras import hangman_dictionary

class Hangman:
    GAME_NAME = "Hangman"
    VERSION = "0.0.1"

    def __init__(self):
        self._board = []
        self._word2catch = ""
        self._board_size = []
        self._catched_letters = []
        self._attempts = 0
        self._a_round = 0
        self._selected_word_len = 0
        self._order_players_moves = {}
        self.hagman_art_id = 0
        self._win = False
        self._end = False

    def start(self) -> None:
        """
            Define the initial values needed to be able 
            to start the game
        """
        self._win = False
        self._end = False
        self._word2catch =  [i for i in hangman_dictionary[randrange(0, len(hangman_dictionary))]]
        self._selected_word_len = len(self._word2catch)
        sortedListKeys = list(hangman_art.keys())
        self._board_size = [len(hangman_art[sortedListKeys[-1]].split('\n')),  # Width
                            len(hangman_art[sortedListKeys[-1]].split('\n')[0])] # Height 
        self._attempts = len(sortedListKeys)
        self._catched_letters = [" " for _ in self._word2catch]
        
    def next_move(self, icharacter:str) -> dict:
        """
            Evaluate the inputs from the user for round. and return 
            a dict with the general information of the game.

            :param icharacter: str, Letter from the user 
        """
        if len(icharacter)>1:
            raise ValueError("Unexpected length of characters")

        if icharacter not in self._word2catch:
            self.hagman_art_id += 1
        else:
            self._catched_letters = [icharacter.lower() if icharacter.lower() == self._word2catch[i] else " " for i in range(len(self._word2catch))]
        self._a_round += 1
        self._attempts -= 1
        self.verify_status()
        dic2ret = {'round': self._a_round,
                   "lifes": self._attempts, 
                   "art_id": self.hagman_art_id,
                   "catched_letters": self._catched_letters,
                   "win": self._win,
                   "end": self._end}
        return dic2ret
    
    def verify_status(self):
        """
            Verify if there is a winer or if the game need to finish 
        """
        if self._a_round >= 7:
            self._end = True 
        if sum([1 if self._catched_letters[i] != " " else 0 for i in range(len(self._word2catch))]) == len(self._word2catch):
            self._win = True
        else:
            self._win = False

    def get_board(self):
        """
            Return the board of the game 
        """
        a_art = hangman_art[self.hagman_art_id]
        a_art = a_art.split("\n")
        tmp = []
        for a_row in a_art:
            _tmp = [i for i in a_row if i != "\n"]
            tmp.append(_tmp)
        return tmp

    def get_word2catch(self):
        return "".join(self._word2catch)

    def get_name(self):
        return self.GAME_NAME
    
    def get_player(self) -> int:
        """
            This Hangman is a game for 1 player 
        """
        return 0

    def get_actual_round_id(self) -> int:
        """
            Return the round that is on going
            :return: int, Actual round 
        """
        return self._a_round

    def get_version(self) -> str:
        """
            Return the game version 
            :return: str, game version 
        """
        return self.VERSION

    def restart(self) -> None:
        """
            Set the board to their initial parameters
        """
        self.start()