class Player():
    
    def __init__(self, color):
        self.color = color
        self.pieces = []
        self.captured_pieces = []
        self.check = False
        self.checkmate = False
        self.stalemate = False
        self.is_currently_playing = False


class HumanPlayer(Player):
    
    def __init__(self, color):
        super().__init__(color)
        self.is_currently_playing = False


class ComputerPlayer(Player):

    def __init__(self, color):
        super().__init__(color)
        self.is_currently_playing = False
