
from model import Model

if __name__ == "__main__":
    model = Model()
    model.game_manager.model = model
    model.view.model = model
    model.view.print_menu()