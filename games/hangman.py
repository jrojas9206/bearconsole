"""
HangMan
Model-View implementation 

Date: 231230
Author: Juan Pablo ROJAS 
Requirements: PyQt5
"""
from random import randrange
from extras import hangman_art
from extras import hangman_dictionary

class Hangman:
    GAME_NAME = "Hangman"
    VERSION = "0.0.1"

    def __init__(self):
        self._board = []
        self._board_view = ""
        self._word2catch = ""
        self._board_size = []
        self._attempts = 0
        self._a_round = 0
        self._selected_word_len = 0
        self._order_players_moves = {}
    
    def start(self):
        self._word2catch =  hangman_dictionary[randrange(0, len(hangman_dictionary))]
        self._selected_word_len = len(self._word2catch)
        sortedListKeys = list(hangman_art.keys())
        self._board_size = [len(hangman_art[sortedListKeys[-1]].split('\n')),  # Width
                            len(hangman_art[sortedListKeys[-1]].split('\n')[0])] # Height 
        self._attempts = len(sortedListKeys)
        
        print(self._board_size)
h = Hangman()
h.start()