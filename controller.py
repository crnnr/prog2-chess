from algorithm import GameAI
import sys
import os
from pathlib import Path
import pathlib
from pieces import *

class GameManager:
   
    def __init__(self, view):
        self.model = None
        self.view = view
        self.ai = None
        self.user_ai = None
        self.load_game = False

    def get_after_game_choice(self):
        
        choice = input('Rematch? (Y/N)')
        if choice.lower() == 'y':
            self.view.clear_console()
            self.start_game()
        elif choice.lower() == 'n':
            self.view.clear_console()
            self.view.print_menu()
        else:
            print('Invalid input!')
            self.get_after_game_choice()

    def get_menu_choice(self):
        
        selection = input('Please enter the number that corresponds to your desired menu: ')

        if selection == '1':
            num_player = input('Enter number of players [1-2]: ')
            if num_player == '1':
                self.model.ai = True
                self.user_ai = GameAI(self.model, self.view, "Black", "White")
                self.model.show_symbols = self.get_symbol_preference()
                self.start_game()
            elif num_player == '2':
                self.model.ai = False
                self.model.show_symbols = self.get_symbol_preference()
                self.start_game()
            else:
                print('Your choice is not valid! Please try again!')
                self.get_menu_choice()

        elif selection == '2':
            pass                # game loading stuff goes here i guess

        elif selection == '3':
            self.model.view.clear_console()
            sys.exit()

        else:
            print('Your choice is not valid! Please try again!')
            self.get_menu_choice()

    def start_game(self):
        if not self.load_game:
            self.model.set_initial_pieces()
            self.view.last_board = self.model.get_copy_board_state()
        else:
            for _ in range(64):
                if self.model.board_state[_] is not None:
                    self.model.pieces.append(self.model.board_state[_])

        self.model.view.update_board()
        self.get_input()

        if self.model.ai:
            while self.model.check_for_king():
                if self.model.currently_playing == 'Black':
                    self.user_ai.move()
                else:
                    self.get_input()
        else:
            while self.model.check_for_king():
                self.get_input()

        print(self.model.currently_playing + ' lost because his king died!')
        self.get_after_game_choice()

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

    def get_input(self):
        
        choice = input('Please enter your desired Move e.g. "e2e4" (type "s" to save): ').upper()

        if choice == "Q":
            self.model.view.clear_console()
            sys.exit()

        if choice == "S":
            pass                # Needs some savintg logic stuff

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