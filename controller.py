import sys
import os

class GameManager:
    """Class that handles everything for the module"""

    def __init__(self, view):
        self.view = view
        self.model = None
        self.user_ai = None
        
    def get_menu_choice(self):
        """Gets input from user and processes the input"""
        selection = self.view.get_user_input('Please enter the number that corresponds to your desired menu: ')
        if selection == '1':
            num_player = self.view.get_user_input('Enter number of players [1-2]: ')
            if num_player == '1':
                self.model.ai = True
                self.model.show_symbols = self.get_symbol_preference()
                self.view.display_message('Player vs AI')
        elif selection == '2':
            self.model.ai = False
            self.model.show_symbols = self.get_symbol_preference()
            self.start_game()
        elif selection == '3':
            self.view.clear_console()
            sys.exit()
        else:
            print('Your choice is not valid! Please try again!')
            self.get_menu_choice()

    def start_game(self):
        for _ in range(64):
            if self.model.board_state[_] is not None:
                self.model.pieces.append(self.model.board_state[_])

    def get_input(self):
        
        choice = input('Please enter your desired Move e.g. "e2e4" (type "s" to save): ').upper()

        if choice == "Q":
            self.model.view.clear_console()
            sys.exit()

        if choice == "S":
            self.view.display_message('I guess you want to save the game. But we are not there yet.')

        if choice == "M":
            self.view.clear_console()
            self.view.print_menu()

        if len(choice) < 4:
            print('Invalid Choice')
            self.get_input()
        else:
            lines = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
            columns = ['1', '2', '3', '4', '5', '6', '7', '8']
            start_pos = choice[:2]
            goal_pos = choice[-2:]
            if start_pos[0] in lines and goal_pos[0] in lines and start_pos[1] in columns and goal_pos[1] in columns:
                self.model.move_piece(self.model.correlation[start_pos], self.model.correlation[goal_pos])
            else:
                print('Invalid Choice')
                self.get_input()

    @staticmethod
    def get_symbol_preference():
        
        while True:
            choice = input('Do you want to use symbols? If not, letters will be used instead. (Y/N): ')
            if choice.lower() == 'y' or choice.lower() == 'yes':
                return True
            elif choice.lower() == 'n' or choice.lower() == 'no':
                return False
            else:
                print('Invalid input! Please answer the question with "yes" or "no"')

    def list_saved_games(self):
        """List all saved games in the saved_games directory."""
        saved_games_dir = 'saved_games'
        saved_games = os.listdir(saved_games_dir)
        if len(saved_games == 0):
            self.view.display_message('No saved games found!')
        else:
            for game in saved_games:
                print(game)
            return saved_games