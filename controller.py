import sys
import os
import datetime
import json
from pathlib import Path
from algorithm import GameAI
from pieces import Rook, Knight, Bishop, Queen, King, Pawn
from view import GameView

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
            choice = GameView.get_user_input('Do you want to use symbols? If not, letters will be used instead. (Y/N): ')
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
            self.view.display_message('No saved games found!')
        else:
            for game in saved_games:
                GameView.display_message(game)
            return saved_games
        
    def save_gamestate(self):
        """Save the current game state to a file."""
        save_name = self.view.get_user_input("Please enter a name for the save file: "
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
            'currently_playing': self.model.currently_playing,
            'show_symbols': self.model.show_symbols,
            'board_state': {str(i): self.piece_to_dict(self.model.board_state[i]) for i in range(64)},
            'ai': self.model.ai
        }

        try:
            with open(filename, 'w', encoding='utf-8') as file:
                json.dump(gamestate, file, indent=4)
                self.view.display_message(f"Game saved as {filename}")
        except IOError as e:
            self.view.display_message(f"Failed to save game: {e}")

    def load_gamestate(self):
        """Load a game state from a file."""
        saved_games = self.list_saved_games()
        if saved_games is None:
            return  # Return to the main menu or handle appropriately
        try:
            selection = int(self.view.get_user_input('Please enter the number of the game to load: '))
            game_save_path = saved_games[selection - 1] 
        except (IndexError, ValueError):
            self.view.display_message("Invalid selection. Please try again.")
            self.load_gamestate()

        
        if game_save_path.exists() and game_save_path.is_file():
            self.view.display_message(f"Loading game from {game_save_path}")
            with game_save_path.open("r") as file:
                GameSave = json.load(file)
                # Set the current player and symbol preference
                self.model.currently_playing = GameSave['currently_playing']
                self.model.show_symbols = GameSave['show_symbols']
                self.load_game = True
                self.user_ai = GameAI(self.model, self.view, "Black", "White")

                if 'Ai' in GameSave:
                    self.ai = True
                    self.model.ai = True

                for i in range(64):
                    # If the piece is None, the position is empty
                    if GameSave['board_state'][str(i)]['piece'] == 'None':  # Moved wird nicht übernommen
                        self.model.board_state[i] = None
                    else:
                        # If the piece is not None, create a new piece object
                        if GameSave['board_state'][str(i)]['piece'] == 'Rooks':
                            self.model.board_state[i] = Rook(GameSave['board_state'][str(i)]['colour'],
                                                             i, self.model)
                        if GameSave['board_state'][str(i)]['piece'] == 'Knights':
                            self.model.board_state[i] = Knight(GameSave['board_state'][str(i)]['colour'],
                                                              i, self.model)
                        if GameSave['board_state'][str(i)]['piece'] == 'Bishops':
                            self.model.board_state[i] = Bishop(GameSave['board_state'][str(i)]['colour'],
                                                               i, self.model)
                        if GameSave['board_state'][str(i)]['piece'] == 'Queens':
                            self.model.board_state[i] = Queen(GameSave['board_state'][str(i)]['colour'],
                                                              i, self.model)
                        if GameSave['board_state'][str(i)]['piece'] == 'Kings':
                            self.model.board_state[i] = King(GameSave['board_state'][str(i)]['colour'],
                                                             i, self.model)
                        if GameSave['board_state'][str(i)]['piece'] == 'Pawns':
                            self.model.board_state[i] = Pawn(GameSave['board_state'][str(i)]['colour'],
                                                             i, self.model)
                
        else:
            self.view.display_message("There's no Save File for your Game!")
            return False

        self.view.last_board = self.model.get_copy_board_state()
        return True

