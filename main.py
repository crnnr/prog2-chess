from controller import Controller
from view import GameView

if __name__ == "__main__":
    game_view = GameView(None)
    controller = Controller(game_view)
    game_view.controller = controller  # Set the controller after initialization
    game_view.clear_console()
    game_view.print_menu()
