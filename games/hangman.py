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
        self._a_round = 0
        self._order_players_moves = {}
    
    def start(self):
        self._word2catch =  hangman_dictionary[randrange(0, len(hangman_dictionary))]
        print(self._word2catch)
h = Hangman()
h.start()