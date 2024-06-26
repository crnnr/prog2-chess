from abc import ABCMeta, abstractmethod
import math

class Piece(metaclass=ABCMeta):

    def __init__(self):
        self.player = None
        self.symbol = None
        self.color = None
        self.moved = False
        self.position = None

    @abstractmethod
    def check_legal_move(self, position):
        pass

    def check_occupied_friendly(self, position, state):
        """Checks if the given position on the chessboard is occupied by a friendly piece."""
        if position in range(64):
            if state[position] is not None:
                if state[position].color == self.player.currently_playing:
                    return True
                else:
                    return False
            else:
                return False
        else:
            return False

    def check_occupied_hostile(self, position, state):
        """Checks if the given position on the chessboard is occupied by an enemy piece. """
        if position in range(64):
            if state[position] is not None:
                if state[position].color != self.player.currently_playing:
                    return True
                else:
                    return False
            else:
                return False
        else:
            return False

    def check_occupied(self, position, state):
        """Checks if a given position on the chessboard is occupied by a piece."""
        if position in range(64):
            if self.check_occupied_hostile(position, state) or self.check_occupied_friendly(position, state):
                return True
            else:
                return False
        else:
            return False

    def check_linear(self, state):
        """Checks for allowed moves in a linear direction (up, down, left, right) for the current piece."""
        allowed = []

        main_row = math.floor(self.position / 8)
        main_column = self.position - (main_row * 7) - main_row

        space_to_check = self.position - 8

        while space_to_check in range(64):
            if not self.check_occupied_friendly(space_to_check, state):
                if self.check_occupied_hostile(space_to_check, state):
                    allowed.append(space_to_check)
                    break
                else:
                    allowed.append(space_to_check)
                    space_to_check = space_to_check - 8
            else:
                break

        space_to_check = self.position + 8

        while space_to_check in range(64):
            if not self.check_occupied_friendly(space_to_check, state):
                if self.check_occupied_hostile(space_to_check, state):
                    allowed.append(space_to_check)
                    break
                else:
                    allowed.append(space_to_check)
                    space_to_check = space_to_check + 8
            else:
                break

        space_to_check = self.position - 1
        column = -1

        while space_to_check in range(64):

            if main_column == 0 or column == 0:
                break

            row = math.floor(space_to_check / 8)
            column = space_to_check - (row * 7) - row

            if not self.check_occupied_friendly(space_to_check, state):
                if self.check_occupied_hostile(space_to_check, state):
                    allowed.append(space_to_check)
                    break
                else:
                    allowed.append(space_to_check)
                    space_to_check = space_to_check - 1
            else:
                break

        space_to_check = self.position + 1

        column = -1

        while space_to_check in range(64):

            if main_column == 7 or column == 7:
                break

            row = math.floor(space_to_check / 8)
            column = space_to_check - (row * 7) - row

            if not self.check_occupied_friendly(space_to_check, state):
                if self.check_occupied_hostile(space_to_check, state):
                    allowed.append(space_to_check)
                    break
                else:
                    allowed.append(space_to_check)
                    space_to_check = space_to_check + 1
            else:
                break
        return allowed

    def check_diagonal(self, state):
        """Checks for allowed moves in a diagonal direction for the current piece."""
        allowed = []

        main_row = math.floor(self.position / 8)
        main_column = self.position - (main_row * 7) - main_row

        space_to_check = self.position - 9
        row = main_row
        column = main_column
        while space_to_check in range(64):

            old_row = row
            old_column = column
            row = math.floor(space_to_check / 8)
            column = space_to_check - (row * 7) - row

            if row < old_row and column < old_column:

                if not self.check_occupied_friendly(space_to_check, state):
                    if self.check_occupied_hostile(space_to_check, state):
                        allowed.append(space_to_check)
                        break
                    else:
                        allowed.append(space_to_check)
                        space_to_check = space_to_check - 9
                else:
                    break
            else:
                break

        row = main_row
        column = main_column
        space_to_check = self.position + 9
        while space_to_check in range(64):

            old_row = row
            old_column = column
            row = math.floor(space_to_check / 8)
            column = space_to_check - (row * 7) - row

            if row > old_row and column > old_column:

                if not self.check_occupied_friendly(space_to_check, state):
                    if self.check_occupied_hostile(space_to_check, state):
                        allowed.append(space_to_check)
                        break
                    else:
                        allowed.append(space_to_check)
                        space_to_check = space_to_check + 9
                else:
                    break
            else:
                break

        row = main_row
        column = main_column
        space_to_check = self.position - 7
        while space_to_check in range(64):

            old_row = row
            old_column = column
            row = math.floor(space_to_check / 8)
            column = space_to_check - (row * 7) - row

            if row < old_row and column > old_column:

                if not self.check_occupied_friendly(space_to_check, state):
                    if self.check_occupied_hostile(space_to_check, state):
                        allowed.append(space_to_check)
                        break
                    else:
                        allowed.append(space_to_check)
                        space_to_check = space_to_check - 7
                else:
                    break
            else:
                break

        row = main_row
        column = main_column
        space_to_check = self.position + 7
        while space_to_check in range(64):

            old_row = row
            old_column = column
            row = math.floor(space_to_check / 8)
            column = space_to_check - (row * 7) - row

            if row > old_row and column < old_column:

                if not self.check_occupied_friendly(space_to_check, state):
                    if self.check_occupied_hostile(space_to_check, state):
                        allowed.append(space_to_check)
                        break
                    else:
                        allowed.append(space_to_check)
                        space_to_check = space_to_check + 7
                else:
                    break
            else:
                break
        return allowed

class Pawn(Piece):
    
    def __init__(self, colour, position, model):
        Piece.__init__(self)
        self.model = model
        self.colour = colour
        self.symbol = self.set_symbol()
        self.position = position
        self.moved = False
        Pawn.table = [
            [0, 0, 0, 0, 0, 0, 0, 0],
            [5, 10, 10, -20, -20, 10, 10, 5],
            [5, -5, -10, 0, 0, -10, -5, 5],
            [0, 0, 0, 20, 20, 0, 0, 0],
            [5, 5, 10, 25, 25, 10, 5, 5],
            [10, 10, 20, 30, 30, 20, 10, 10],
            [50, 50, 50, 50, 50, 50, 50, 50],
            [0, 0, 0, 0, 0, 0, 0, 0]
        ]

    def set_symbol(self):
        if self.model.show_symbols:
            if self.colour == 'White':
                return '\u2659'
            else:
                return '\u265F'
        else:
            if self.colour == 'White':
                return 'P'
            else:
                return 'p'

    def check_legal_move(self, position, state="", return_all=False):
        """Checks if the move is legal for the pawn piece."""
        allowed = []
        if state == "":
            state = self.model.board_state

        row = math.floor(self.position / 8)
        column = self.position - (row * 7) - row

        if self.colour == 'White':
            if not self.check_occupied(self.position - 8, state):
                allowed.append(self.position - 8)
            if self.check_occupied_hostile(self.position - 9, state) and column != 0:
                allowed.append(self.position - 9)
            if self.check_occupied_hostile(self.position - 7, state) and column != 7:
                allowed.append(self.position - 7)
            if not self.moved:
                if not self.check_occupied(self.position - 16, state) and\
                        not self.check_occupied(self.position - 8, state):
                    allowed.append(self.position - 16)
        else:
            if not self.check_occupied(self.position + 8, state):
                allowed.append(self.position + 8)
            if self.check_occupied_hostile(self.position + 9, state) and column != 7:
                allowed.append(self.position + 9)
            if self.check_occupied_hostile(self.position + 7, state) and column != 0:
                allowed.append(self.position + 7)
            if not self.moved:
                if not self.check_occupied(self.position + 16, state) and\
                        not self.check_occupied(self.position + 8, state):
                    allowed.append(self.position + 16)

        if return_all:
            return allowed

        if position in allowed:
            return True
        else:
            return False

    def upgrade(self):
        if self.colour == 'Black':
            if self.position in range(56, 63):
                return True
            else:
                return False
        else:
            if self.position in range(0, 7):
                return True
            else:
                return False

class Rook(Piece):
    def __init__(self, color, position):
        super().__init__()
        self.symbol = self.set_symbol()
        self.color = color
        self.position = position

    def set_symbol(self):
        """
        Sets the symbol for the chess piece based on its color.
        Returns:
        str: The Unicode symbol representing the chess piece.
        """
        if self.color == 'White':
            return '\u265C'
        else:
            return '\u2656'
    
    def check_legal_move(self, position, state="", return_all=False):
        """Checks if the move is legal for the rook piece."""
        allowed = []

        if state == "":
            state = self.model.board_state

        allowed += self.check_linear(state)

        if return_all:
            return allowed

        if position in allowed:
            return True
        else:
            return False

class Knight(Piece):

    def __init__(self, color, position):
        super().__init__()
        self.symbol = self.set_symbol()
        self.color = color
        self.position = position

    def set_symbol(self):
        """
        Sets the symbol for the chess piece based on its color.

        Returns:
            str: The Unicode symbol representing the chess piece.
        """
        if self.color == 'White':
            return '\u265E'
        else:
            return '\u2658'

    def check_legal_move(self, position, state="", return_all=False):
        allowed = []

        if state == "":
            state = self.model.board_state

        row = math.floor(self.position / 8)
        column = self.position - (row * 7) - row

        if not self.check_occupied_friendly(self.position - 17, state) and row >= 2 and column >= 1:
            allowed.append(self.position - 17)
        if not self.check_occupied_friendly(self.position - 15, state) and row >= 2 and column <= 6:
            allowed.append(self.position - 15)
        if not self.check_occupied_friendly(self.position - 10, state) and row >= 1 and column >= 2:
            allowed.append(self.position - 10)
        if not self.check_occupied_friendly(self.position - 6, state) and row >= 1 and column <= 5:
            allowed.append(self.position - 6)
        if not self.check_occupied_friendly(self.position + 17, state) and row <= 5 and column <= 6:
            allowed.append(self.position + 17)
        if not self.check_occupied_friendly(self.position + 15, state) and row <= 5 and column >= 1:
            allowed.append(self.position + 15)
        if not self.check_occupied_friendly(self.position + 10, state) and row <= 6 and column <= 5:
            allowed.append(self.position + 10)
        if not self.check_occupied_friendly(self.position + 6, state) and row <= 6 and column >= 2:
            allowed.append(self.position + 6)
        if return_all:
            return allowed

        if position in allowed:
            return True
        else:
            return False


class Bishop(Piece):

        def __init__(self, color, position):
            super().__init__()
            self.symbol = self.set_symbol()
            self.color = color
            self.position = position

        def set_symbol(self):
            """
            Sets the symbol for the chess piece based on its color.

            Returns:
            str: The Unicode symbol representing the chess piece.
            """
            if self.color == 'White':
                return '\u265D'
            else:
                return '\u2657'

        def check_legal_move(self, position, state="", return_all=False):
            """Checks if the move is legal for the bishop piece."""
            if state == "":
                state = self.model.board_state

            allowed = self.check_diagonal(state)

            if return_all:
                return allowed
            if position in allowed:
                return True
            else:
                return False

class Queen(Piece):
     
    def __init__(self, colour, position, model):
        Piece.__init__(self)
        self.model = model
        self.colour = colour
        self.symbol = self.set_symbol()
        self.position = position

    def set_symbol(self):
        """
        Sets the symbol for the chess piece based on its color.
        Returns:
        str: The Unicode symbol representing the chess piece.
        """
        if self.color == 'White':
            return '\u265B'
        else:
            return '\u2655'

    def check_legal_move(self, position, state="", return_all=False):
        """Checks if the move is legal for the queen piece."""
        if state == "":
            state = self.model.board_state

        allowed = self.check_linear(state) + self.check_diagonal(state)
        if return_all:
            return allowed
        if position in allowed:
            return True
        else:
            return False

class King(Piece):
    def __init__(self, color, position):
        super().__init__()
        self.symbol = self.set_symbol()
        self.color = color
        self.position = position
    def set_symbol(self):
        """
        Sets the symbol for the chess piece based on its color.
        Returns:
        str: The Unicode symbol representing the chess piece.
        """
        if self.color == 'White':
            return '\u265A'
        else:
            return '\u2654'
    def check_legal_move(self, position, state="", return_all=False):
        """Checks if the move is legal for the king piece."""
        allowed = []

        if state == "":
            state = self.model.board_state

        if not self.check_occupied_friendly(self.position - 9, state):
            allowed.append(self.position - 9)
        if not self.check_occupied_friendly(self.position - 8, state):
            allowed.append(self.position - 8)
        if not self.check_occupied_friendly(self.position - 7, state):
            allowed.append(self.position - 7)
        if not self.check_occupied_friendly(self.position - 1, state):
            allowed.append(self.position - 1)
        if not self.check_occupied_friendly(self.position + 1, state):
            allowed.append(self.position + 1)
        if not self.check_occupied_friendly(self.position + 7, state):
            allowed.append(self.position + 7)
        if not self.check_occupied_friendly(self.position + 8, state):
            allowed.append(self.position + 8)
        if not self.check_occupied_friendly(self.position + 9, state):
            allowed.append(self.position + 9)
        if return_all:
            return allowed
        if position in allowed:
            return True
        else:
            return False