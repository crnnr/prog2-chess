#from view import GameView
import sys

class Controller:
    """Class that handles everything for the module"""

    def __init__(self):
        pass
        
    def get_menu_choice(self):
        """Gets input from user and processes the input"""
        selection = input('Please enter the number that corresponds to your desired menu: ')
        if selection == '1':
            print('1')
        elif selection == '2':
            print('2')
        elif selection == '3':
            print('3')
        elif selection == '4':
            #GameView.clear_console()
            sys.exit()
        else:
            print('Your choice is not valid! Please try again!')
            self.get_menu_choice()

