class GameView:

    def __init__(self):
        pass

    def print_menu(self):
        self.clear_console()
        print(""" 
  ██████╗██╗  ██╗███████╗███████╗███████╗
 ██╔════╝██║  ██║██╔════╝██╔════╝██╔════╝
 ██║     ███████║█████╗  ███████╗███████╗
 ██║     ██╔══██║██╔══╝  ╚════██║╚════██║
 ╚██████╗██║  ██║███████╗███████║███████║
  ╚═════╝╚═╝  ╚═╝╚══════╝╚══════╝╚══════╝
      by Christof & Manuel                                 
""")
        print("""      Welcome to Chess:
      1) New Game
      2) Load Game
      3) Exit
""")