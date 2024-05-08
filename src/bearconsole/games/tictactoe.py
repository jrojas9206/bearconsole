"""
Tic Tac Toe 
Model-View implementation 

Date: 231230
Author: Juan Pablo ROJAS 
Requirements: PyQt5
"""
import sys 

class TicTacToe:

    GAME_NAME = "Tictactoe"
    VERSION = "0.0.2"

    def __init__(self, player1:str="X", player2:str="O"):
        self._board = []
        self._board_view = ""
        self._a_round = 0
        self._order_players_moves = {}
        if player1 == "|" or player2 == "|":
            raise IOError(" The character | is reserved, choose another character")
        self._iplayer1 = player1 
        self._iplayer2 = player2
        self.gameStatus = {}
        self.start()

    def get_requirements(self) -> dict:
        """
            Get the main definitions need it from the user
            this is useful for the Menu Object 
        """
        return {
            "nplayers": 2,
            "player_input": [int, str],
            "player_board_reference": ["row", "column"],
            "playerReference":"character",
            "range":[[1,3], ["A", "C"]],
            "initLogo": ["~(x-O)P", "~(O-x)P"]
        }

    def start(self) -> None:
        """
            Create a lista that represent 
            the board with which the user will
            interact 

            :param self._board: list, List that represent the board to work  
        """
        rows = 5
        columns = 5
        columns_names = [" A", " ", "B", " ", "C"]
        rows_names = ["1 ", "  ", "2 ", "  ", "3 "]
        self._board = []
        self._order_players_moves = {a_round_f: 0 if a_round_f%2 == 0 else 1 for a_round_f in  range(10)}
        # Create the list to work. each character 
        # in the tic tac toe's row is related to a position in the list.
        # Each row of the keyboard is a sublist  
        self._board.append([" "]+columns_names)
        for row in range(rows):
            tmp = []
            if row%2 != 0:
                self._board.append(["  "]+["-" for _ in range(column+1)])
                continue
            for column in range(columns):
                if column == 0:
                    tmp.append(rows_names[row])
                if column%2 != 0:
                    tmp.append("|")
                else:
                    tmp.append(" ")
            self._board.append(tmp)

    def update(self, player:dict) -> None:
        """
          Update the keyboard base on the 
          player movement 
          :param player: dict, Dictionary that represent
          the player action 
          :NOTE:
            player = {
                playerID: int  # 0 or 1
                playerSelection: list # coordinates [row:int, columns:str]
            }
        """
        ref_dict = {"A": 1, "B":3, "C":5}
        if player["playerSelection"][0]<1 or player["playerSelection"][0]>3:
             raise ValueError("Index %i is outside of range for a object with length 3" %(player["playerSelection"][0]))
        row2update = player["playerSelection"][0]+(player["playerSelection"][0]-1)
        column2update = ref_dict[player["playerSelection"][1]]
        if self._board[row2update][column2update] != " ":
            raise Warning("[WARNING] this position was already selected")
         
        self._board[row2update][column2update] = self._iplayer1 if player["playerID"] == 0 else self._iplayer2
        self.gameStatus = self.verifyBoard()

    def get_gamestatus(self) -> dict:
        """
            General information about the game 
        """
        return self.gameStatus

    def verifyBoard(self) -> dict:
        """
            Verify if there is winner in row or column 
        """
        d2ret = {
                "winner": 0, # The player id 
                "allLose": False, # The expected round are over 
                "end":False,
                "isColumn": False, 
                "nPos": -1,
                }
        cntr = 0
        for playerID, a_player in enumerate([self._iplayer1, self._iplayer2], start=1):
            for idx, actual in enumerate(self._board):
                # row verification
                tmp = [1 if stat == a_player else 0 for stat in actual] 
                if sum(tmp) == 3:
                    d2ret["winner"] = playerID
                    d2ret["nPos"] = idx
                    d2ret["end"] = True
                    return d2ret
                # Column verification 
                tmp_v = [1 if self._board[i][idx] == a_player else 0  for i in range(len(self._board))] 
                if sum(tmp_v) == 3:
                    d2ret["winner"] = playerID
                    d2ret["nPos"] = idx
                    d2ret["isColumn"] = True
                    d2ret["end"] = True
                    return d2ret
                cntr += sum(tmp)
                if cntr==9:
                    d2ret["winner"] = 0
                    d2ret["nPos"] = 0
                    d2ret["isColumn"] = False
                    d2ret["allLose"] = True
                    d2ret["end"] = True
                    return d2ret  
            # Diagonal 
            # Left to right
            tmp = []
            for a_idx in range(1,4):
                board_idex = a_idx + (a_idx-1)
                tmp.append(self._board[board_idex][board_idex])

            tmp = [1 if stat == a_player else 0 for stat in tmp]
            if sum(tmp) == 3:
                d2ret["winner"] = playerID
                d2ret["nPos"] = idx
                d2ret["end"] = True
                return d2ret                

            tmp = []
            for a_idx in range(3, 0, -1):
                board_idex = a_idx + (a_idx-1)
                tmp.append(self._board[6-board_idex][board_idex])
            tmp = [1 if stat == a_player else 0 for stat in tmp]
            if sum(tmp) == 3:
                d2ret["winner"] = playerID
                d2ret["nPos"] = idx
                d2ret["end"] = True
                return d2ret 

        d2ret = {"winner": 0,
                 "isColumn": False,
                 "nPos": -1,
                 "allLose": False,
                 "end":False,}
    
        return  d2ret
    
    def next_move(self, newrow_pos:int, newcolumn:str) -> None:
        """
            Automatic handler for the rounds along the game
            this method get as input a move and automatically asing it 
            to the player that must play in this round 
        """
        player_move = {
                "playerID": self._order_players_moves[self._a_round],  # 0 or 1
                "playerSelection": [newrow_pos ,newcolumn] # coordinates [row:int, columns:str]
        }
        self.update(player_move)
        self._a_round += 1
        if self._a_round>=10:
            raise ValueError("Unexpected number of matches!!")

    def get_player(self) -> int:
        """
            This player returns the player that have to make the move
            in the actual round
            :return: int, Player that need to make the move
        """
        return self._order_players_moves[self._a_round]

    def get_board(self) -> list:
        """
            Get the list that represent the board
            :return: list, Game representation 
        """
        return self._board

    def get_name(self) -> str:
        """
            Return the game name
            :return: str
        """
        return self.GAME_NAME

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

    def get_player_symbole(self):
        return self._iplayer1, self._iplayer2

    def get_menu(self):
        print("Work in progress")