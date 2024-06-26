from player import HumanPlayer, ComputerPlayer
from pieces import Rook, Knight, Bishop, Queen, King, Pawn

class GameBoard:
    """Class that handles the game board"""

    def __init__(self):
        self.board_state = [None] * 64

    def set_initial_pieces(self):
       """Set the initial pieces on the board"""
       positions = {'Rook': [0, 7, 56, 63], 'Knight': [1, 6, 57, 62], 'Bishop': [2, 5, 58, 61],
                    'Queen': [3, 59], 'King': [4, 60]}
       for piece, places in positions.items():
           for position in places:
               color = 'White' if position > 7 else 'Black'
               self.board_state[position] = globals()[piece](color, position, self)
       for i in range(8):
           self.board_state[8 + i] = Pawn('Black', 8 + i, self)
           self.board_state[48 + i] = Pawn('White', 48 + i, self)
       for pos in range(16, 48):
           self.board_state[pos] = None
       self.pieces = [piece for piece in self.board_state if piece is not None]

    def _update_positions(self, piece, start_pos, goal_pos, update):
        """Update the positions of the pieces on the board"""
        killed_piece = self.board_state[goal_pos]
        self.board_state[goal_pos], self.board_state[start_pos] = piece, None
        piece.position = goal_pos
        if isinstance(piece, Pawn) and piece.upgrade():
            self.board_state[goal_pos] = Queen(self.currently_playing, goal_pos, self)
        if killed_piece:
            self.pieces.remove(killed_piece)
        piece.moved = True

    def check_for_king(self):
        """Check if the king is alive on the board"""
        king_alive = False
        for i in self.pieces:
            if type(i) == King and i.colour == self.currently_playing:
                king_alive = True
                break
        return king_alive

    def get_copy_board_state(self, state=None):
        """Get a copy of the board state"""
        if state is None:
            state = self.board_state
        return state.copy()