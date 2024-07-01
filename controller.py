import sys
import os
from pathlib import Path
from datetime import datetime
import json
from view import GameView
from pieces import *
from player import HumanPlayer, ComputerPlayer


class GameManager:
   
    def __init__(self, view):
        self.board = None
        self.view = view
        self.ai = None
        self.player_white = None
        self.player_black = None
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
            num_player = GameView.input_prompt('Enter number of players [1-2]: ')
            if num_player == '1':
                self.board.ai = True
                self.player_white = HumanPlayer('White', self.view)
                self.player_black = ComputerPlayer('Black', self.board, self.view, 'White')
                self.board.show_symbols = self.get_symbol_preference()
                self.start_game()
            elif num_player == '2':
                self.board.ai = False
                self.player_white = HumanPlayer('White', self.view)
                self.player_black = HumanPlayer('Black', self.view)
                self.board.show_symbols = self.get_symbol_preference()
                self.start_game()
            else:
                GameView.display_message('Your choice is not valid! Please try again!')
                self.get_menu_choice()

        elif selection == '2':
            self.load_gamestate()
            self.start_game()

        elif selection == '3':
            self.view.clear_console()
            sys.exit()

        else:
            GameView.display_message('Your choice is not valid! Please try again!')
            self.get_menu_choice()

    def start_game(self):
        if not self.load_game:
            self.board.set_initial_pieces()
            self.view.last_board = self.board.get_copy_board_state()
        else:
            for _ in range(64):
                if self.board.board_state[_] is not None:
                    self.board.pieces.append(self.board.board_state[_])

        self.view.update_board()
        self.get_input()

        if self.board.ai:
            while self.board.check_for_king():
                if self.board.currently_playing == 'Black':
                    self.player_black.make_move(self.board)
                else:
                    self.get_input()
        else:
            while self.board.check_for_king():
                self.get_input()

        GameView.display_message(self.board.currently_playing + ' lost because his king died!')
        self.get_after_game_choice()

    @staticmethod
    def get_symbol_preference():
        
        while True:
            choice = GameView.input_prompt('Do you want to use symbols? If not, letters will be used instead. (Y/N): ')
            if choice.lower() == 'y' or choice.lower() == 'yes':
                return True
            elif choice.lower() == 'n' or choice.lower() == 'no':
                return False
            else:
                GameView.display_message('Invalid input! Please answer the question with "yes" or "no"')

    def get_input(self):
        
        choice = GameView.input_prompt('Please enter your desired Move e.g. "e2e4" (type "s" to save): ').upper()

        if choice == "Q":
            self.board.view.clear_console()
            sys.exit()

        if choice == "S":
            self.save_gamestate()
            self.view.clear_console()
            self.view.print_menu()
            self.get_menu_choice()

        if choice == "M":
            self.view.clear_console()
            self.view.print_menu()

        if len(choice) < 4:
            GameView.display_message('Invalid Choice')
            self.get_input()
        else:
            lines = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
            columns = ['1', '2', '3', '4', '5', '6', '7', '8']
            start_pos = choice[:2]
            goal_pos = choice[-2:]
            if self.ai == False:
                if self.board.currently_playing == 'White':
                    if start_pos[0] in lines and goal_pos[0] in lines and start_pos[1] in columns and goal_pos[1] in columns:
                        self.player_white.make_move(self.board.correlation[start_pos], self.board.correlation[goal_pos], self.board)
                    else:
                        GameView.display_message('Invalid Choice')
                        self.get_input()
                else:
                    if start_pos[0] in lines and goal_pos[0] in lines and start_pos[1] in columns and goal_pos[1] in columns:
                        self.player_black.make_move(self.board.correlation[start_pos], self.board.correlation[goal_pos], self.board)
                    else:
                        GameView.display_message('Invalid Choice')
                        self.get_input()
    @staticmethod
    def get_symbol_preference():
        
        while True:
            choice = GameView.input_prompt('Do you want to use symbols? If not, letters will be used instead. (Y/N): ')
            if choice.lower() == 'y' or choice.lower() == 'yes':
                return True
            elif choice.lower() == 'n' or choice.lower() == 'no':
                return False
            else:
                GameView.display('Invalid input! Please answer the question with "yes" or "no"')

    def list_saved_games(self):
        """List all saved games in the saved_games directory."""
        saved_games_dir = 'saved_games'
        saved_games = os.listdir(saved_games_dir)
        if len(saved_games == 0):
            GameView.display_message('No saved games found!')
        else:
            for game in saved_games:
                GameView.display_message(game)
            return saved_games
        
    def save_gamestate(self):
        """Save the current game state to a file."""
        save_name = GameView.input_prompt("Please enter a name for the save file: "
                          "(leave blank for a timestamped filename): ")
        
        if not save_name:
            save_name = datetime.now().strftime("%Y-%m-%d_%H-%M-%S") + ".json"
        else:
            if not save_name.endswith(".json"):
                save_name += ".json"
        #OS independent path
        filename = Path("saved_games", save_name)
        self.create_directory_if_not_exists()
        
        gamestate = {
            'currently_playing': self.board.currently_playing,
            'show_symbols': self.board.show_symbols,
            'board_state': {str(i): self.piece_to_dict(self.board.board_state[i]) for i in range(64)},
            'ai': self.board.ai
        }

        try:
            with open(filename, 'w', encoding='utf-8') as file:
                json.dump(gamestate, file, indent=4)
                GameView.display_message(f"Game saved as {filename}")
        except IOError as e:
            GameView.display_message(f"Failed to save game: {e}")

    def load_gamestate(self):
        """Load a game state from a file."""
        saved_games = self.list_saved_games()
        if saved_games is None:
            return  # Return to the main menu or handle appropriately
        try:
            selection = int(GameView.input_prompt('Please enter the number of the game to load: '))
            game_save_path = saved_games[selection - 1] 
        except (IndexError, ValueError):
            GameView.display_message("Invalid selection. Please try again.")
            self.load_gamestate()

        
        if game_save_path.exists() and game_save_path.is_file():
            GameView.display_message(f"Loading game from {game_save_path}")
            with game_save_path.open("r") as file:
                GameSave = json.load(file)
                # Set the current player and symbol preference
                self.board.currently_playing = GameSave['currently_playing']
                self.board.show_symbols = GameSave['show_symbols']
                self.load_game = True
                self.player_black = ComputerPlayer('Black', self.board, self.view, 'White')

                if 'Ai' in GameSave:
                    self.ai = True
                    self.board.ai = True

                for i in range(64):
                    # If the piece is None, the position is empty
                    if GameSave['board_state'][str(i)]['piece'] == 'None':  # Moved wird nicht übernommen
                        self.board.board_state[i] = None
                    else:
                        # If the piece is not None, create a new piece object
                        if GameSave['board_state'][str(i)]['piece'] == 'Rooks':
                            self.board.board_state[i] = Rook(GameSave['board_state'][str(i)]['colour'],
                                                             i, self.board)
                        if GameSave['board_state'][str(i)]['piece'] == 'Knights':
                            self.board.board_state[i] = Knight(GameSave['board_state'][str(i)]['colour'],
                                                              i, self.board)
                        if GameSave['board_state'][str(i)]['piece'] == 'Bishops':
                            self.board.board_state[i] = Bishop(GameSave['board_state'][str(i)]['colour'],
                                                               i, self.board)
                        if GameSave['board_state'][str(i)]['piece'] == 'Queens':
                            self.board.board_state[i] = Queen(GameSave['board_state'][str(i)]['colour'],
                                                              i, self.board)
                        if GameSave['board_state'][str(i)]['piece'] == 'Kings':
                            self.board.board_state[i] = King(GameSave['board_state'][str(i)]['colour'],
                                                             i, self.board)
                        if GameSave['board_state'][str(i)]['piece'] == 'Pawns':
                            self.board.board_state[i] = Pawn(GameSave['board_state'][str(i)]['colour'],
                                                             i, self.board)
                
        else:
            GameView.display_message("There's no Save File for your Game!")
            return False

        self.view.last_board = self.board.get_copy_board_state()
        return True