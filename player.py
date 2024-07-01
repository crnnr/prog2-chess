from view import GameView
from algorithm import GameAI


class Player():
    
    def __init__(self, color):
        self.color = color
        self.pieces = []
        self.captured_pieces = []
        self.is_currently_playing = False

    def make_move(self, board):
        """Abstract method to be implemented by subclasses to make a move."""
        raise NotImplementedError("Subclasses must implement this method")


class HumanPlayer(Player):
    
    def __init__(self, color, view):
        super().__init__(color)
        self.view = view

    def make_move(self, start_pos, goal_pos, board, update=True):
        """Method to make a move."""
        piece = board.board_state[start_pos]
        if piece and piece.colour == self.color:
            if piece.check_legal_move(goal_pos):
                board.update_positions(piece, start_pos, goal_pos, update)
                board.toggle_player()
            else:
                GameView.display_message('Illegal move! Please try again!')
                self.game_manager.get_input()
        else:
            GameView.display_message('There is no piece of your color on this space. Please try again!')
            self.game_manager.get_input()
        if update:
            self.view.update_board()


class ComputerPlayer(Player):

    def __init__(self, color, board, view, enemy):
        super().__init__(color)
        self.is_currently_playing = False
        self.game_ai = GameAI(board, view, color, enemy)
        self.view = view

    def make_move(self):
        """Method to make a move."""
        self.game_ai.move()
        self.view.update_board()