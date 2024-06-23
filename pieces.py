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
            return '\u265F'
        else:
            return '\u2659'

    def check_legal_move(self, position):
        pass

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
                return '\u265E'
        else:
                return '\u2658'

    def check_legal_move(self, position):
        pass

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

    def check_legal_move(self, position):
        pass

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

        def check_legal_move(self, position):
            pass

    class Queen(Piece):

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
                return '\u265B'
            else:
                return '\u2655'

        def check_legal_move(self, position):
            pass

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

        def check_legal_move(self, position):
            pass