from view import GameView
from controller import GameManager
from pieces import Pawn, King, Queen

class Model:

    def __init__(self):
        self.board_state = [None] * 64
        self.view = GameView()
        self.game_manager = GameManager(self.view)
        self.show_symbols = True
        self.correlation = {f"{chr(65 + col)}{8 - row}": row * 8 + col for row in range(8) for col in range(8)}
        self.pieces = []
        self.currently_playing = 'White'
        self.ai = None
        self.set_initial_pieces()

    def set_initial_pieces(self):
        # Set the initial pieces on the board
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

    def toggle_player(self):
        if self.currently_playing == 'White':
            self.currently_playing = 'Black'
        else:
            self.currently_playing = 'White'

    def move_piece(self, start_pos, goal_pos, update=True):
        piece = self.board_state[start_pos]
        if piece and piece.colour == self.currently_playing:
            if piece.check_legal_move(goal_pos):
                self._update_positions(piece, start_pos, goal_pos, update)
                self.toggle_player()
            else:
                print('Illegal move! Please try again!')
                self.game_manager.get_input()
        else:
            print('There is no piece of your color on this space. Please try again!')
            self.game_manager.get_input()
        if update:
            self.view.update_board()

    def _update_positions(self, piece, start_pos, goal_pos, update):
        killed_piece = self.board_state[goal_pos]
        self.board_state[goal_pos], self.board_state[start_pos] = piece, None
        piece.position = goal_pos
        if isinstance(piece, Pawn) and piece.upgrade():
            self.board_state[goal_pos] = Queen(self.currently_playing, goal_pos, self)
        if killed_piece:
            self.pieces.remove(killed_piece)
        piece.moved = True

    def check_for_king(self):
        king_alive = False
        for i in self.pieces:
            if type(i) == King and i.colour == self.currently_playing:
                king_alive = True
                break
        return king_alive

    def get_copy_board_state(self, state=None):
        if state is None:
            state = self.board_state
        return state.copy()