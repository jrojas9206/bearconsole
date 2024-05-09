"""
Generic terminal board 
The model creates a string that represent 
the board of the game and displayed

Date: 231230
Author: Juan Pablo ROJAS 
Requirements: PyQt5
"""

import sys 
import time 
import os 
class Menu:
    def __init__(self, game:dict, board):
        self.iBoard = board
        self.i_gameID =  -1
        self.lstGames = game
        self.selectedGame = ""
        self._game_requirements = {}

    def start_menu(self):
        lck = True
        state = 0 
        os.system('cls' if os.name == 'nt' else 'clear')
        while(lck):
            if state == 0:
                print("Welcome to PLadventure")
                print(" -> Games to play:")
                for a_game_id in self.lstGames.keys():
                    print("  -> %s: %s" %(a_game_id, self.lstGames[a_game_id].get_name()))
                print(" -> to quit the game press q")
                userInput = input("- Please chose the game you want to play: ")
                if userInput == "q":
                    lck = False
                    continue
                self.i_gameID = int(userInput) 
                state += 1
            elif state == 1:
                self.selectedGame = self.lstGames[self.i_gameID]
                self.iBoard.load_game(self.selectedGame)
                self._game_requirements = self.selectedGame.get_requirements()
                status = self.runGame()
                state += 1
            else:
                print("---END---")
                time.sleep(2)
                self.clean_terminal()
                state = 0

    def clean_terminal(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def runGame(self):
        runGame = True
        stateGame = 0
        active_player = 0
        position = []
        player_lst = []
        initAnimationTime = 5
        idx_init_msg = 0
        player_character = []
        init_message = ""
        self.clean_terminal()
        while(runGame):
            print("gameState", stateGame)
            if stateGame == 0:
                # This could be set in the board class not it in the menu 
                while(initAnimationTime>0):
                    os.system('cls' if os.name == 'nt' else 'clear')
                    init_message = """
                    %s
                    Welcome to %s
                    %s%s
                    %s
                    """ %("#"*(11+len(self.iBoard.get_game_name())), 
                        self.iBoard.get_game_name(),
                        " "*int(((11+len(self.iBoard.get_game_name()))/2)-(len(self._game_requirements["initLogo"][idx_init_msg])/2)),
                        self._game_requirements["initLogo"][idx_init_msg],
                        "#"*(11+len(self.iBoard.get_game_name())))
                    print(init_message)
                    idx_init_msg += 1
                    if idx_init_msg >= len(self._game_requirements["initLogo"]):
                        idx_init_msg = 0
                    initAnimationTime -= 1
                    time.sleep(0.5)
                print(" -> Select your character (^-^)/")
                for a_player in range(self._game_requirements["nplayers"]):
                    generic_input = input("  -> Player %s select the %s to play:" %((a_player+1) if self._game_requirements["nplayers"]==2 else "",
                                                                   self._game_requirements["playerReference"],
                                                                   ))
                    player_character.append(generic_input)
                print(" -> Be ready! the game will start!!")
                time.sleep(0.5)
                self.clean_terminal()
                stateGame += 1
            if stateGame == 1:
                self.clean_terminal()
                print(init_message)
                self.iBoard.display_board()
                player_movements = []
                for idx_player in range(self._game_requirements["nplayers"]):
                    player_movements = []
                    for a_input in self._game_requirements["player_board_reference"]:
                        generic_input = input("  -> Player %s [%s] please select the %s for your actual movement: " %( idx_player+1, 
                                                                      player_character[idx_player],
                                                                      a_input))
                        if(generic_input == "q"):
                            sys.exit()
                        player_movements.append(generic_input)
                    self.clean_terminal()
                    print(init_message)
                    if len(self._game_requirements["player_board_reference"]) == 2:
                        self.iBoard.next_move(int(player_movements[0]), player_movements[1])
                    elif len(self._game_requirements["player_board_reference"]) == 1:
                         self.iBoard.next_move(column=player_movements[0])
                    self.iBoard.display_board()
                    gameGeneralStatus = self.iBoard.get_game_status()
                    if(gameGeneralStatus["winner"] != 0):
                        print("***Congratulations Player %s you have won!!" %(gameGeneralStatus["winner"] if self._game_requirements["nplayers"]==2 else "")) 
                        stateGame += 1
                        break
                    if(gameGeneralStatus["allLose"]):
                        print("***There is no winners in this game!! Try again!!")
                        stateGame += 1
                        break

                    if stateGame>=2:
                        break        
            if stateGame >= 2:
                runGame = False
                break 
        return gameGeneralStatus
