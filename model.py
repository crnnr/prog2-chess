from view import GameView


class Model:

    def __init__(self, view):
        self.view = view
        self.ai = None
        self.show_symbols = True