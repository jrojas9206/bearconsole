"""
Tic Tac Toe 
Model-View implementation 

Date: 231230
Author: Juan Pablo ROJAS 
PyQt
"""
import sys 

class TicTacToe:
    def __init__(self, player1:str="X", player2:str="O"):
        self._board = []
        self._board_view = ""
        if player1 == "|" or player2 == "|":
            raise IOError(" The character | is reserved, choose another character")
        self._iplayer1 = player1 
        self._iplayer2 = player2
        self.gameStatus = {}
        self.start()

    def get_requiremets(self):
        return {
            "player1":str,
            "player2":str
        }

    def start(self):
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

    def update(self, player:dict):
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
        self._board[row2update][column2update] = self._iplayer1 if player["playerID"] == 0 else self._iplayer2
        self.gameStatus = self.verifyBoard()

    def get_gamestatus(self):
        """
            General information about the game 
        """
        return self.gameStatus

    def verifyBoard(self):
        """
            Verify if there is winner in row or column 
        """
        d2ret = {"winner": 0,
                 "isColumn": False,
                 "nPos": -1,
                 "allLose": False}
        cntr = 0
        for playerID, a_player in enumerate([self._iplayer1, self._iplayer2], start=1):
            for idx, actual in enumerate(self._board):
                # row verification
                tmp = [1 if stat == a_player else 0 for stat in actual] 
                if sum(tmp) == 3:
                    d2ret["winner"] = playerID
                    d2ret["nPos"] = idx
                    return d2ret
                # Column verification 
                tmp_v = [1 if self._board[i][idx] == a_player else 0  for i in range(len(self._board))] 
                if sum(tmp_v) == 3:
                    d2ret["winner"] = playerID
                    d2ret["nPos"] = idx
                    d2ret["isColumn"] = True
                    return d2ret
                cntr += sum(tmp)
                if cntr==9:
                    d2ret["winner"] = 0
                    d2ret["nPos"] = 0
                    d2ret["isColumn"] = False
                    d2ret["allLose"] = True
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
                return d2ret                

            tmp = []
            for a_idx in range(3, 0, -1):
                board_idex = a_idx + (a_idx-1)
                tmp.append(self._board[6-board_idex][board_idex])
            tmp = [1 if stat == a_player else 0 for stat in tmp]
            if sum(tmp) == 3:
                d2ret["winner"] = playerID
                d2ret["nPos"] = idx
                return d2ret 

        d2ret = {"winner": 0,
                 "isColumn": False,
                 "nPos": -1,
                 "allLose": False}
    
        return  d2ret
    
    def get_board(self):
        """
            Get the list that represent the board
        """
        return self._board

    def restart(self):
        """
            Set the board to their initial parameters
        """
        self.start()

class Board:
    """
        Class to visualize the tic tac toe 
        in the terminal     
    """
    def __init__(self):
        self._game_board_ = "ttt"

    def set_model(self, model):
        self._board = model.get_board()

    def prepare_board(self):
        """
            Print the board in its actual state 
        """
        a_board = ""
        for a_row in self._board:
            a_board += "".join(a_row+["\n"])
        self._board_view = a_board

    def display_board(self):
        self.prepare_board()
        print(self._board_view)


class Menu:
    def __init__(self, game, board):
        self.iBoard = board
        self.i_gameID =  -1
        self.lstGames = {0: game}
        self.selectedGame = ""

    def start_menu(self):
        lck = True
        state = 0 
        while(lck):
            if state == 0:
                print("Welcome to PLadventure")
                print(" -> Games to play:\n  -> [0] TicTacToe")
                print(" -> to quit the game press q")
                userInput = input("- Plese chose the game you want to play: ")
                if userInput == "q":
                    lck = False
                    continue
                self.i_gameID = int(userInput) 
                state += 1
            elif state == 1:
                self.selectedGame = self.lstGames[self.i_gameID]
                status = self.runGame()
                state += 1
            else:
                print(status)
                print("Finish")
                state = 0

    def runGame(self):
        runGame = True
        stateGame = 0
        active_player = 0
        rowOK = False
        columnOk = False 
        while(runGame):
            if stateGame==0:
                print("#"*10)
                print("Welcome to TicTacToe!! |O_X|/-")
                print("#"*10)
                player1_def = input("Player 1: Choose your character to play: ")
                player2_def = input("Player 2: Choose your character to play: ")
                if player1_def == "q" or player2_def == "q":
                    sys.exit()
                print(" %s VS %s" %(player1_def, player2_def))
                self.iBoard.set_model(self.selectedGame)
                self.iBoard.display_board()
                stateGame=1
            elif stateGame == 1:
                if active_player <= 1:
                    if not rowOK:
                        row = input("Player %i select the row for your movement: " %(active_player+1))
                    if row == "q":
                        sys.exit()
                    try:
                        row = int(row)
                        rowOK = True
                    except ValueError:
                        print("[Warning] Select a number between 1 to 3, letters are not accecpter")
                        continue
                    if not columnOk:
                        column = input("Player %i select the column for your movement: " %(active_player+1))
                    if column == "q":
                        sys.exit()
                    player = {
                            'playerID': active_player,  # 0 or 1
                            'playerSelection': [row, column] # coordinates [row:int, columns:str]
                    }
                    try:
                        self.selectedGame.update(player)
                        columnOk = True
                    except KeyError:
                        print("[Warning] Value outside of the board. Available Option: A,B,C")
                        continue
                    self.iBoard.display_board()
                    statusGame = self.selectedGame.get_gamestatus()
                    if statusGame["winner"] != 0:
                        print(" ### The winner is Player %i ###" %(statusGame["winner"]))
                        stateGame+=1
                        
                    if statusGame["allLose"]:
                        print("  ### No Winner (^-^)/& ###")
                        stateGame+=1
                    active_player+=1
                    rowOK = False
                    columnOk = False
                elif active_player > 1:
                    active_player = 0
            else:
                runGame = False
        return statusGame    
                    

def main():
    ttt = TicTacToe()
    tttboard = Board()

    amenu = Menu(ttt, tttboard)
    amenu.start_menu()
    # ttt = TicTacToe()
    # ttt.start()
    # board = Board(ttt)
    # # board.display_board()
    # player = {
    # "playerID": 0,  # 0 or 1
    # "playerSelection": [3,"A"] # coordinates [x, y]
    # }
    # ttt.update(player)
    # board.display_board()
    # player = {
    # "playerID": 0,  # 0 or 1
    # "playerSelection": [2,"B"] # coordinates [x, y]
    # }
    # ttt.update(player)
    # player = {
    # "playerID": 0,  # 0 or 1
    # "playerSelection": [1,"C"] # coordinates [x, y]
    # }
    # ttt.update(player)
    # board.display_board()

    return 0 

if __name__ == "__main__":
    sys.exit(main())