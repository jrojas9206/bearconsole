"""
HangMan
Model-View implementation 

Date: 231230
Author: Juan Pablo ROJAS 
Requirements: PyQt5
"""
from random import randrange
from bearconsole.games.tanimation.extras import hangman_art
from bearconsole.games.tanimation.extras import hangman_dictionary

class Hangman:
    GAME_NAME = "Hangman"
    VERSION = "0.0.1"

    def __init__(self) -> None:
        self._board = []
        self._word2catch = ""
        self._board_size = []
        self._catched_letters = []
        self._attempts = 0
        self._errors_usr = 0
        self._a_round = 0
        self._used_letters = []
        self._selected_word_len = 0
        self._order_players_moves = {}
        self.hagman_art_id = 0
        self._game_status_ = {}
        self._win = False
        self._end = False

    def get_requirements(self) -> dict:
        """
            Return a dict with the minimum elements
            to start the game 
            :return: dict
        """
        return {
            "nplayers": 1,
            "player_input": [str],
            "player_board_reference": ["letter"],
            "playerReference":"symbole",
            "range":[["A", "Z"]],
            "initLogo": ["_(-=-)_", "-(^_^)-", "\\(O_O)/"]
        }

    def start(self) -> None:
        """
            Define the initial values needed to be able 
            to start the game
        """
        self._win = False
        self._end = False
        self._used_letters = []
        self._a_round = 0
        self.hagman_art_id = 0
        self._word2catch =  [i for i in hangman_dictionary[randrange(0, len(hangman_dictionary))]]
        self._selected_word_len = len(self._word2catch)
        sortedListKeys = list(hangman_art.keys())
        self._board_size = [len(hangman_art[sortedListKeys[-1]].split('\n')),  # Width
                            len(hangman_art[sortedListKeys[-1]].split('\n')[0])] # Height 
        self._attempts = len(sortedListKeys)
        self._catched_letters = [" " for _ in self._word2catch]
        self._game_status_ = {
                   "winner":1 if self._win  else 0,
                   "allLose": self._end,
                   'round': self._a_round,
                   "lifes": self._attempts, 
                   "art_id": self.hagman_art_id,
                   "catched_letters": self._catched_letters,
                   }

    def next_move(self, icharacter:str) -> dict:
        """
            Evaluate the inputs from the user for round. and return 
            a dict with the general information of the game.

            :param icharacter: str, Letter from the user 
        """
        self._used_letters.append(icharacter)
        if len(icharacter)>1:
            raise ValueError("Unexpected length of characters")

        if icharacter not in self._word2catch:
            self.hagman_art_id += 1
            self._attempts -= 1
        else:
            for idx, a_letter in enumerate(self._word2catch):
                if icharacter.lower() == a_letter and self._catched_letters[idx] == " ":
                    self._catched_letters[idx] = icharacter

            #self._catched_letters = [icharacter.lower() if (icharacter.lower() == self._word2catch[i] and self._catched_letters[i] == " ") else " " for i in range(len(self._word2catch))]
        self._a_round += 1
        self.verify_status()
        
        self._game_status_ = {
                   "winner":1 if self._win  else 0,
                   "allLose": self._end,
                   'round': self._a_round,
                   "lifes": self._attempts, 
                   "art_id": self.hagman_art_id,
                   "catched_letters": self._catched_letters,
                   }
    
    def verify_status(self) -> None:
        """
            Verify if there is a winer or if the game need to finish 
        """
        if self.hagman_art_id == len(list(hangman_art.keys()))-1:
            self._end = True 
        if sum([1 if self._catched_letters[i] != " " else 0 for i in range(len(self._word2catch))]) >= len(self._word2catch):
            self._win = True
        else:
            self._win = False

    def get_gamestatus(self) -> dict:
        """
            Return the game resume in the actual round
            :return dict:
        """
        return self._game_status_

    def get_board(self) -> list[str,str]:
        """
            Return the list that represent the board of the game 
            :return: list[str, str, ...]
        """
        a_art = hangman_art[self.hagman_art_id]
        a_art = a_art.split("\n")
        tmp = []
        for a_row in a_art:
            _tmp = [i for i in a_row if i != "\n"]
            tmp.append(_tmp)

        usr_catches = [' ']+["_" if i==" " else i for i in self._catched_letters]+[' ']
        tmp.append(["#"*(len(self._word2catch)+2)])
        tmp.append(usr_catches)
        tmp.append(["#"*(len(self._word2catch)+2)])
        return tmp

    def get_word2catch(self) -> str:
        """
            Return the word to catch in the actual game
            :return: str
        """
        return "".join(self._word2catch)

    def get_name(self) -> str:
        """
            Return the game name
            :return: str
        """
        return self.GAME_NAME
    
    def get_player(self) -> int:
        """
            This Hangman is a game for 1 player 
            :return: int
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

    def get_used_letters(self) -> str:
        """
            Retrun the string with the used letters
            :return: str
        """
        return "[%s]"%("-".join(list(set(self._used_letters))))

    def restart(self) -> None:
        """
            Restart the game parameters
        """
        self.start()