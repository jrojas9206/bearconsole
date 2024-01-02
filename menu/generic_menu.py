import sys 

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