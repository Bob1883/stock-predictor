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
    t.add_rows([['Options', 'Description'], 
                ['1', 'Get data'], 
                ['2', 'Check data'], 
                ['3', 'Models'], 
                ['4', 'Train model'], 
                ['5', 'Make prediction'], 
                ['6', 'HELP'], 
                ['7', 'Exit                                                               ']])
    table_output = t.draw()

    print(table_output)

# TODO: integrate the webscraping scripts
def get_data():
    running = True
    while running:
        os.system('cls' if os.name == 'nt' else 'clear')
        print("What type of data would you like to get?")

        # use the texttable package to create a table
        t = Texttable(max_width=100)
        t.add_rows([['Options', 'Description'], 
                    ['1', 'Get historical data'], 
                    ['2', 'Get commodity data'],
                    ['3', 'Get google trends data'],
                    ['4', 'Get news data'],
                    ['5', 'Get social media data'],
                    ['6', 'Get political data'],
                    ['7', 'Get world data'],
                    ['8', 'Back to start home                                               ']])
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
        '7': lambda: print("You selected option 7"),
        '8': lambda: print("going back to start menu..."),
        }

        os.system('cls' if os.name == 'nt' else 'clear')

        if option in option_actions:
            if option == '7':
                running = False
            else:
                option_actions[option]()
                time.sleep(1)
        else:
            os.system('cls' if os.name == 'nt' else 'clear')
            print("Invalid option selected. Please type a number between 1 and 7")
            time.sleep(3)

def check_data():
    pass

def train_model():
    running = True
    while running:
        print("Would you like to continue training or create a new model?")
        answer = input("Please type 'c' to continue training or 'n' to create a new model: ")
        if answer == 'c':
            while True:
                print("What model would you like to use?")
                models = []
                for os.path in os.listdir("models"):
                    if os.path.isfile(os.path):
                        models.append(os.path)
                print("The following models are available:")
                for i, model in enumerate(models):
                    print(f"{i+1}. {model}")
                model = input(f"Please type the name of the model you want to use (1-{len(models)}): ")
                os.system('cls' if os.name == 'nt' else 'clear')
                if model in models:
                    print(f"Training model {model}...")
                    # train_model(model)
                    print(f"Model {model} has been trained.")
                    running = False
                    break
                else:
                    print("\033[91mInvalid model. Please type the name of the model you want to use.\033[0m")
                    time.sleep(2)

        elif answer == 'n':
            print("What would you like to name the model?")
            model = input("Please type the name of the model you want to create: ")

            print("Do you want to use default settings?")
            print("Default settings:")
            print("Model:", model)
            print("Data:", "All available")
            print("Prediction:", "Close")
            print("Excluded companies:", "None")
            print("Years:", "3")
            print("Max trials:", "5")
            print("Max runs:", "3")
            print("Epochs:", "100")
            print("Batch size:", "32")
            print("Max neurons:", "512")
            print("Optimizer:", "Adam")
            print("Loss function:", "Mean Squared Error")
            print("Metrics:", "Mean Squared Error")
            answer = input("Would you like to edit the settings? (y/n): ")

            if answer == 'y':
                print("\nWhat data do you want to use?")
                inc = input("Please type the name of the data you want to use: ")

                print("\nWhat Would you like to predict?")
                pred = input("Please type the name of the data you want to predict: ")

                print("\nWhat commpanies would you like to exclude from the training data?")
                exc = input("Please type the name of the companies you want to exclude: ")

                print("\nHow many days would you like the model to train on?")
                print("Note that it depends on how much data you have.")
                print("Some data like political is limited by the source. EX: political")
                years = input("Please type the number of years you want the model to train on: ")

                os.system('cls' if os.name == 'nt' else 'clear')

                print("How many trails would you like to run?")
                print("Note that it can take a significant amount of time to train a model. So keep the number low.")
                max_trials = input("Please type the number of trials you want to run: ")

                print("How many runs per trial would you like to run?")
                print("Note that it can take a significant amount of time to train a model. So keep the number low.")
                max_runs = input("Please type the number of runs you want to run: ")

                print("How many epochs would you like to run?")
                epochs = input("Please type the number of epochs you want to run: ")

                print("what is the batch size?")
                batch_size = input("Please type the batch size: ")

                print("What is the max number of neurons should a layer have?")
                max_neurons = input("Please type the max number of neurons: ")

                print("What optimizer would you like to use?")
                optimizer = input("Please type the optimizer you want to use: ")

                print("What loss function would you like to use?")
                loss = input("Please type the loss function you want to use: ")

                print("What metrics would you like to use?")
                metrics = input("Please type the metrics you want to use: ")

            print("starting training...")
            # train_model(model, inc, pred, exc, days, max_trials, max_runs, epochs, batch_size, max_neurons, optimizer, loss, metrics)
            print(f"Model {model} has been trained.")
            running = False
            break   
        
        else:
            print("\033[91mInvalid input. Please type 'c' or 'n'.\033[0m")
            time.sleep(2)

def make_prediction():
    pass

def help():
    print("Start with adding the data by using option 1. You only need to get the data you want.")
    print("Then proceed to check the data by using option 2 so that there is nothing missing.")
    print("The code will automatically fix the problems, but if there is somthing that cant be fixed, it will be shown.")
    print("After that, you can train the model by using option 4. You will get multiple options. These include:")
    # TODO: add the options for training the model
    print("After training the model, you can make a prediction by using option 5.")
    print("If you want to check the models you have created, use option 3.")
    print("If you want to exit the program, use option 7.")

    input("Press enter to go back to the start menu...")
  
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
            '6': lambda: help(),
            '7': lambda: exit("Goodbye!")
        }

        if option in option_actions:
            option_actions[option]()
            time.sleep(1)
        else:
            os.system('cls' if os.name == 'nt' else 'clear')
            print("Invalid option selected. Please type a number between 1 and 7")
            time.sleep(2)