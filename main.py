# King Jordan's Coffee Shop Simulator 4000
# Copyright 2026 Universal Source Code LLC, All Rights Reserved.

# Written by Creg Clarence Sullivan Senior Principal Software Engineer.

# Import all functions from the utlity module
# Provide a local fallback for `prompt()` to avoid depending on an external `utilities` module.

import pickle
import re
from pathlib import Path

# Import the game class from the  coffee_shop_simulator module
from coffee_shop_simulator import CoffeeShopSimulator

print("Welcome to King Jordan's Coffee Shop Simulator 4000!, Version 1.00")
print("Copyright 2026 Universal Source Code LLC, All Rights Reserved.\n")

# If saved file exists, see if the player wants to load it
run_game = True

if Path(CoffeeShopSimulator.SAVE_FILE).is_file():
    # Save game exists, do they want to load it?
    response = CoffeeShopSimulator.prompt("There's a saved game. Do you want to load it? (Y/N): ", True)
    if re.search("y", response, re.IGNORECASE):
        # Load the game and run!
        with open(CoffeeShopSimulator.SAVE_FILE, mode= "rb") as f:
            game = pickle.load(f)
        game.run()
        #We don't need to run the game again
        run_game = False
    else:
        print("Hint: If you don't want to see this prompt again, remove the CoffeeShopSimulator.SAVE_FILE + \n")
        
if run_game:
    # Create the game object and run it!
    game = CoffeeShopSimulator()
    game.run()
    
	#Say goodbye!
    print("\nThanks for playing King Jordan's Coffee Shop Simulator 4000! Goodbye!\n")