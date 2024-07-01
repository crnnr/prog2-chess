from board import GameBoard

if __name__ == "__main__":
    board = GameBoard()
    board.game_manager.board = board
    board.view.model = board
    board.view.print_menu()