import sys 
import math 
import numpy as np 

class DotAndBoxes:

    GAME_NAME="Dot and boxes"

    def __init__(self, board_size:list=[9,9], player_1:str="X", player_2:str="O") -> None:
        self._round = 0 
        self._active_player = 0
        self._taked_coord = []
        self._end = False,
        self._move_symbol = {}
        self._player_1 = player_1
        self._player_2 = player_2
        self._next_round = True
        self._game_status_ = {
                   "winner":-1,
                   "allLose": False,
                   'round': 0,
                   "art_id": 0,
                   "boxes": [],
                   }
        self._board_size = [(2*i) for i in board_size] 
        self._box2finish = (self._board_size[0]/2)*(self._board_size[1]*2)
        self._requirements = {
            "nplayers": 2,
            "player_input": [int, int],
            "player_board_reference": ["point_init", "point_end"],
            "playerReference":"symbole",
            "range":[[self._board_size[0], self._board_size[1]], [self._board_size[0], self._board_size[1]]],
            "initLogo": ["o", "o-", "o-o", "(*-*)", "(*-*)/"]
        }
        self._fixed_point = self._requirements["nplayers"]+1 # Point that the user can select and connect
        self._connection_point = self._requirements["nplayers"]+2 # connection path that will change when the user connect two points
        self._board = np.zeros(self._board_size, dtype=np.int8)+self._connection_point
        self._draw_board = []

    def _init_board(self):
        self._board = np.zeros(self._board_size, dtype=np.int8)+self._connection_point
        self._game_status_ = {
                   "winner":-1,
                   "allLose": False,
                   'round': 0,
                   "art_id": 0,
                   "boxes": [],
                   }
        self._move_symbol = {}
        self._draw_board = []
        for row in range(1, self._board_size[0]):
            if row == 1:
                self.set_board_axis(1)
                self.set_board_axis(0)
            for column in range(1, self._board_size[1]):
                if row%2 != 0 and column%2!=0:
                    self._board[row, column] = self._fixed_point
        self.draw_board()

    def set_board_axis(self, axis:int) -> None:
        cntr = 1
        for idx in range(self._board_size[axis]):
            if idx % 2 != 0:
                self._board[0 if axis==1 else idx, 0 if axis==0 else idx] = cntr
                cntr += 1
            else:
                self._board[0 if axis==1 else idx, 0 if axis==0 else idx] = self._connection_point

    def next_move(self, row:list, column:list):
        # Real posicion in the array of used as board 
        p1_x, p1_y = (row[0]*2)-1, (column[0]*2)-1
        p2_x, p2_y = (row[1]*2)-1, (column[1]*2)-1
        distance = math.sqrt( ((p2_x-p1_x)**2) + ((p2_y-p1_y)**2) )   
        if (len(set(row)) == 2 and len(set(column))==2) or distance>2:
            raise ValueError("Unexpected move: You can do only linear movements, and with a distance lower than 1")
        if (p1_x>self._board.shape[0] or p2_x>self._board.shape[0] or
            p1_y>self._board.shape[1] or p2_y>self._board.shape[1]):
            raise Warning("Movement outside of the board")
        coordinate2draw = lambda pi, pe: (pi+pe)-1
        if p1_x == p2_x and p1_y != p2_y:
            self._board[p1_x, coordinate2draw(column[0], column[1])] = self.get_player()
            self._move_symbol["%i_%i"%(p1_x, coordinate2draw(column[0], column[1]))] = "-"
        elif p1_x != p2_x and p1_y == p2_y:
            self._board[coordinate2draw(row[0], row[1]), p1_y,] = self.get_player()
            self._move_symbol["%i_%i"%(coordinate2draw(row[0], row[1]), p2_y)] = "|"
        # The verification of the taken box and the verification of next round is done in 
        # verify_statys()
        self.verify_status()
        self._round += 1

    def taked_box_rounds_list(self) -> list:
        lst2ret = []
        if  len(self._taked_coord)>0:
            for a_take in self._taked_coord:
                lst2ret.append(a_take["round"])
            return lst2ret
        return []

    def verify_status(self):
        init_coord = [2,2]
        end_coord = [self._board_size[0]-1, self._board_size[1]-1]
        cntr = 0
        _input_round = self.get_actual_round_id()
        _input_player = self.get_player()
        for idx, center_row_idx in enumerate(range(init_coord[0], end_coord[0], 2)):
            for center_column_idx in range(init_coord[1], end_coord[1], 2):
                if (self._board[center_row_idx, center_column_idx-1] != self._connection_point and
                    self._board[center_row_idx, center_column_idx+1] != self._connection_point and
                    self._board[center_row_idx+1, center_column_idx] != self._connection_point and
                    self._board[center_row_idx-1, center_column_idx] != self._connection_point):
                    cntr += 4
                if cntr == 4 and not self.is_taken([center_row_idx, center_column_idx])[0]:
                    self._taked_coord.append({"player":_input_player, 
                                            "coordinate":[center_row_idx, center_column_idx],
                                            "round": _input_round})
                    self._board[center_row_idx, center_column_idx] = _input_player
                    if _input_round == self.get_actual_round_id():
                        self._round-=1
                cntr = 0

        if  len(self._taked_coord) >= self._box2finish:
            self._end = True

        self._game_status_ = {
                   "winner": self.actual_winner() if self._end else -1,
                   "allLose": self._end,
                   'round': self.get_actual_round_id(),
                   "art_id": None,
                   "boxes": self._taked_coord,
                   }

    def get_actual_round_id(self):
        return self._round

    def actual_winner(self):
        players = {player:0 for player in range(self._requirements["nplayers"])}
        for a_box in self._taked_coord:
            for a_player in players.keys():
                if a_player == a_box["player"]:
                    players[a_player]+=1
        highest_points = 0
        winner = -1
        for a_player, a_points in players.items():
            if a_points > highest_points:
                highest_points = a_points
                winner = a_player 
        return winner


    def start(self):
        self._round = 0
        self._active_player = 0
        self._taked_coord = []
        self._init_board()

    def get_requirements(self):
        return self._requirements

    def get_name(self) -> str:
        return self.GAME_NAME
    
    def get_player(self):
        return 0 if self._round%2 == 0 else 1
    
    def is_taken(self, coord:list) -> [bool, int]:
        for a_taken in self._taked_coord:
            a_coord = a_taken["coordinate"]
            if sum([1 if a==b else 0 for a,b in zip(a_coord, coord)])==2:
                return [True, a_taken["player"]]
        return [False, -1]

    def draw_board(self):
        self._draw_board = []
        for idx0, a_row in enumerate(self._board):
            _tmp = []
            if idx0 == 0:
                _tmp = [" " if i == 0 else ('-' if  i == self._connection_point and iidx%2 == 0 else str(i)) for iidx, i in enumerate(a_row)]
            else:
                for idx1, a_col in enumerate(a_row):
                    if  idx1 == 0:
                        _tmp.append( "|" if a_col == self._connection_point and idx0%2==0 else str(a_col) )
                        continue
                    if a_col == self._fixed_point:
                        _tmp.append("o")
                    elif a_col == self._connection_point:
                        _tmp.append(" ")
                    elif a_col in range(0, self._requirements["nplayers"]):
                        e2search = "%i_%i" %(idx0, idx1)
                        if e2search in self._move_symbol.keys():
                            _tmp.append(self._move_symbol[e2search])
                        else:
                            statTaken = self.is_taken([idx0, idx1])
                            if statTaken[0]:
                                _tmp.append(self._player_1 if statTaken[1]==0 else self._player_2)
                    else:
                        print("There is unknown value in the board, report the bug", idx0, idx1, a_col)

            self._draw_board.append(_tmp) 

    def display_board(self):
        self.draw_board()
        str2plot = ""
        for a_row in self._draw_board:
            str2plot += "%s\n" %(" ".join(a_row))
        print(str2plot)
        print("####### ROUND:%s ########" %(self.get_actual_round_id()))
        print("Player: %i | Symbol: %s" %(self.get_player()+1, self.get_symbol()))
        print("########################")

    def get_symbol(self):
        return self._player_1 if self.get_player() == 0 else self._player_2

    def get_board(self):
        self.draw_board()
        return self._draw_board
    
def simple_menu():
    dab = DotAndBoxes([5,5])
    dab.start()
    for _ in range(25):
        dab.display_board()
        i_coord = input("Introduce your coordinates in the format x1,y1,x2,y2: \n")
        if "q" in i_coord:
            sys.exit()
        x1, y1, x2, y2 = i_coord.split(',')
        dab.next_move([int(x1), int(x2)], [int(y1),int(y2)])
        


if __name__ == "__main__":
    simple_menu()