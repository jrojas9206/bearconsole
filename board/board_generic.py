class Board:
    """
        Class to visualize in the terminal  
        the different games    
    """
    def __init__(self):
        self._game_board_ = "ttt"

    def set_model(self, model):
        """
            Set the game object 

            :param model:
        """
        self._board = model.get_board()

    def set_game_name(self, name:str) -> None:
        self._game_board_ = name

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