class GameView:

    def __init__(self):
        pass


    @staticmethod
    def display_message(message):
        # Display a message to the user
        pass
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