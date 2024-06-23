import os
from controller import GameManager

class GameView:

    def __init__(self):
        self.last_board = None
        self.model = None
        self.controller = GameManager(self)  # Initialize GameManager with a reference to this GameView instance
    
    def update_board(self, state=None):
        self.clear_console()
        state = state or self.model.board_state
        print(f'Current turn: {self.model.currently_playing}\n')
        self.print_board(state)
        self.last_board = self.model.get_copy_board_state()

    def print_board(self, state):
        header = '    ' + '   '.join(' A B C D E F G H'.split())
        lines = [header, self.build_box('top')]

        for i, letter in enumerate('87654321'):
            row = f'{letter} ' + self.format_row(state[i*8:(i+1)*8], i)
            lines.append(row)
            if i != 7:
                lines.append(self.build_box('middle'))
        lines.append(self.build_box('bottom'))
        lines.append(header)

        for line in lines:
            print(line)

    @staticmethod
    def get_background_color(row, col):
        if (row + col) % 2 == 0:
            return '\x1b[48;5;230m\x1b[38;5;16m'  # Light square
        else:
            return '\x1b[48;5;240m\x1b[38;5;16m'  # Dark square
        
    def format_row(self, pieces, row_idx):
        formatted_row = ''
        for col_idx, piece in enumerate(pieces):
            background = self.get_background_color(row_idx, col_idx)
            if piece is not None:
                symbol = f' {piece.symbol} '
                display = f'{background}{symbol}\x1b[0m'
            else:
                display = f'{background}   \x1b[0m'
            formatted_row += f'\u2551{display}'
        return formatted_row + '\u2551'
            
    def build_box(self, part):
        if part == 'top':
            return '  \u2554' + '\u2550\u2550\u2550\u2566' * 7 + '\u2550\u2550\u2550\u2557'
        elif part == 'middle':
            return '  \u2560' + '\u2550\u2550\u2550\u256C' * 7 + '\u2550\u2550\u2550\u2563'
        return '  \u255A' + '\u2550\u2550\u2550\u2569' * 7 + '\u2550\u2550\u2550\u255D'

    @staticmethod
    def display_message(message):
        """
        Display a message to the user.
        """
        print(message)

    @staticmethod
    def get_user_input(prompt):
        """
        Get user input from the console.
        """
        return input(prompt)

    @staticmethod
    def clear_console():
        """
        Clear the console of unnecessary stuff
        """
        if os.name in ['nt', 'dos']:
            command = 'cls'
        else:
            command = 'clear'
        os.system(command)

    def print_menu(self):
        print(""" 
  ██████╗██╗  ██╗███████╗███████╗███████╗
 ██╔════╝██║  ██║██╔════╝██╔════╝██╔════╝
 ██║     ███████║█████╗  ███████╗███████╗
 ██║     ██╔══██║██╔══╝  ╚════██║╚════██║
 ╚██████╗██║  ██║███████╗███████║███████║
  ╚═════╝╚═╝  ╚══════╝╚══════╝╚══════╝
      by Christof & Manuel                                 
""")
        print("""      Welcome to Chess:
      1) New Game
      2) Load Game
      3) Exit
""")
        self.controller.get_menu_choice()