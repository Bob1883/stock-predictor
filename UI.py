# from train_model import train_model 
from texttable import Texttable
import time
import os 

running = True

def start_menu():
    print("""\033[95m
                  ___         ___           ___           ___           ___     
      ___        /\  \       /\  \         /\  \         /\  \         /\__\    
     /\  \      /::\  \      \:\  \       /::\  \       /::\  \       /:/  /    
     \:\  \    /:/\ \  \      \:\  \     /:/\:\  \     /:/\:\  \     /:/__/     
     /::\__\  _\:\~\ \  \     /::\  \   /:/  \:\  \   /:/  \:\  \   /::\__\____ 
  __/:/\/__/ /\ \:\ \ \__\   /:/\:\__\ /:/__/ \:\__\ /:/__/ \:\__\ /:/\:::::\__\\
 /\/:/  /    \:\ \:\ \/__/  /:/  \/__/ \:\  \ /:/  / \:\  \  \/__/ \/_|:|  | 
 \::/__/      \:\ \:\__\   /:/  /       \:\  /:/  /   \:\  \          |:|  |    
  \:\__\       \:\/:/  /   \/__/         \:\/:/  /     \:\  \         |:|  |    
   \/__/        \::/  /                   \::/  /       \:\__\        |:|  |    
                 \/__/                     \/__/         \/__/         \|__|    
    \033[0m""")

    print("Welcome to the Stock Predictor!")

    # use the texttable package to create a table
    t = Texttable(max_width=100)
    t.add_rows([['Options', 'Description'], ['1', 'Get data'], ['2', 'Check data'], ['3', 'Models'], ['4', 'Train model'], ['5', 'Make prediction'], ['6', 'HELP'], ['7', 'Exit                                                               ']])
    table_output = t.draw()

    print(table_output)

def get_data():
    print("What type of data would you like to get?")

    # use the texttable package to create a table
    t = Texttable(max_width=100)
    t.add_rows([['Options', 'Description'], ['1', 'Get historical data'], ['7', 'Back to start screen                                               ']])
    table_output = t.draw()

    print(table_output) 

    option = input("Please select an option: ")

    option_actions = {
    '1': lambda: print("Getting historical data..."),
    '2': lambda: print("You selected option 2"),
    '3': lambda: print("You selected option 3"),
    '4': lambda: print("You selected option 4"),
    '5': lambda: print("You selected option 5"),
    '6': lambda: print("You selected option 6"),
    '7': lambda: exit("Goodbye! (ﾉ◕ヮ◕)ﾉ*:･ﾟ✧")}

    if option in option_actions:
        option_actions[option]()
        time.sleep(1)
    else:
        os.system('cls' if os.name == 'nt' else 'clear')
        print("Invalid option selected. Please type a number between 1 and 7")
        time.sleep(3)
        
if __name__ == "__main__":
    while running:
        os.system('cls' if os.name == 'nt' else 'clear')
        start_menu()
        option = input("Please select an option: ")
        option_actions = {
            '1': lambda: get_data(),
            '2': lambda: print("You selected option 2"),
            '3': lambda: print("You selected option 3"),
            '4': lambda: print("You selected option 4"),
            '5': lambda: print("You selected option 5"),
            '6': lambda: print("You selected option 6"),
            '7': lambda: exit("Goodbye! (ﾉ◕ヮ◕)ﾉ*:･ﾟ✧")
        }

        if option in option_actions:
            option_actions[option]()
            time.sleep(1)
        else:
            os.system('cls' if os.name == 'nt' else 'clear')
            print("Invalid option selected. Please type a number between 1 and 7")
            time.sleep(3)