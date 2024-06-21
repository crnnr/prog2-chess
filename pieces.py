from abc import ABCMeta, abstractmethod

class Piece(metaclass=ABCMeta):

    def __init__(self):
        self.symbol = None
        self.color = None
        self.moved = False
        self.position = None

    @abstractmethod
    def check_legal_move(self, position):
        pass

class Pawn(Piece):

    def __init__(self, color, position):
        super().__init__()
        self.symbol = self.set_symbol()
        self.color = color
        self.position = position

    def set_symbol(self):
        pass  

    def check_legal_move(self, position):
        pass

class Rook(Piece):

    def __init__(self, color, position):
        super().__init__()
        self.symbol = self.set_symbol()
        self.color = color
        self.position = position

    def set_symbol(self):
        pass

    def check_legal_move(self, position):
        pass

class Knight(Piece):

    def __init__(self, color, position):
        super().__init__()
        self.symbol = self.set_symbol()
        self.color = color
        self.position = position

    def set_symbol(self):
        pass

    def check_legal_move(self, position):
        pass

    class Bishop(Piece):

        def __init__(self, color, position):
            super().__init__()
            self.symbol = self.set_symbol()
            self.color = color
            self.position = position

        def set_symbol(self):
            pass

        def check_legal_move(self, position):
            pass

    class Queen(Piece):

        def __init__(self, color, position):
            super().__init__()
            self.symbol = self.set_symbol()
            self.color = color
            self.position = position

        def set_symbol(self):
            pass

        def check_legal_move(self, position):
            pass

    class King(Piece):

        def __init__(self, color, position):
            super().__init__()
            self.symbol = self.set_symbol()
            self.color = color
            self.position = position

        def set_symbol(self):
            pass

        def check_legal_move(self, position):
            pass