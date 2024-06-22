import os
from controller import Controller

class GameView:

    def __init__(self):
        self.controller = Controller()

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
  ╚═════╝╚═╝  ╚═╝╚══════╝╚══════╝╚══════╝
      by Christof & Manuel                                 
""")
        print("""      Welcome to Chess:
      1) New Game
      2) Load Game
      3) Exit
""")
        self.controller.get_menu_choice()