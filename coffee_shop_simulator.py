import pickle
import random
import re
import math
import statistics


class CoffeeShopSimulator:

    # Minimum and maximum temperatures
    Temp_Min = 20
    Temp_Max = 90

    # length of Temperature List
    # (higher produces more realistic curve)
    SERIES_DENSITY = 300

    # Save game file
    SAVE_FILE = "savegame.dat"

    def __init__(self):
        # Get name and store name
        print("Let's collect some information before we start the game.\n")

        # Set player and coffee shop names
        self.player_name = self.prompt("What is your name?", True)

        self.shop_name = self.prompt("What do you want to name your coffee shop?", True)

        # Current day number
        self.day = 1

        # Cash on hand at start
        self.cash = 100.00

        # Inventory at start
        self.coffee_inventory = 100

        # Sales list
        self.sales = []

        # Possible temperatures
        self.temps = self.make_temp_distribution()

    def run(self):
        print("\nOk, let's get started. Have fun")

        # The main game loop
        running = True

        while running:

            # Display the day and a "fancy" text effect
            self.day_header()

            # Get the weather
            temperature = self.weather

            # Display the cash and weather
            self.daily_stats(temperature)

            # Get price of a cup of coffee (but provide an escape hatch)
            response = self.prompt("What do you want to charge per cup of coffee? (type exit to quit)")
            if re.search("^exit", response, re.IGNORECASE):
                # Exit the game loop
                running = False
                continue
            else:
                try:
                    cup_price = int(response)
                except (ValueError, TypeError):
                    print("Invalid price entered; defaulting to $1.")
                    cup_price = 1

                # Do they want to buy more coffee inventory?
                print("\nIt costs $1 for the necessary inventory to make a cup of coffee.")
                response = self.prompt("Want to buy more so you can make more coffee? (Enter for none or number)", False)
                if response:
                    if not self.buy_coffee(response):
                        print("Could not buy additional coffee.")

                # Get advertising spend
                print("\nYou can buy advertising to help promote sales.")
                advertising = self.prompt("How much do you want to spend on advertising today? (0 for none)?", False)

            # Convert advertising into a float
            advertising = self.convert_to_float(advertising)

            # Deduct advertising from cash on hand
            self.cash -= advertising

            # Simulate today's sales
            cups_sold = self.simulate(temperature, advertising, cup_price)
            gross_profit = cups_sold * cup_price

            # Display the results
            print("You sold " + str(cups_sold) + " cups of coffee today.")
            print("You made $" + str(gross_profit) + ".")

            # Add the profit to our coffers
            self.cash += gross_profit

            # Subtract inventory
            self.coffee_inventory -= cups_sold

            if self.cash < 0:
                print("\n:( GAME OVER! You ran out of cash.")
                running = False
                continue

            # Before we loop around, add a day
            self.increment_day()

            # Save the game
            with open(self.SAVE_FILE, mode="wb") as f:
                pickle.dump(self, f)

    def simulate(self, temperature, advertising, cup_price):
        # Find out how many cups were sold
        cups_sold = self.daily_sales(temperature, advertising, cup_price)

        # Save the sales data for today
        self.sales.append({
            "day": self.day,
            "coffee_inv": self.coffee_inventory,
            "advertising": advertising,
            "temp": temperature,
            "cup_price": cup_price,
            "cups_sold": cups_sold
        })

        return cups_sold

    def buy_coffee(self, amount):
        try:
            i_amount = int(amount)
        except (ValueError, TypeError):
            return False
        if i_amount <= self.cash:
            self.coffee_inventory += i_amount
            self.cash -= i_amount
            return True
        else:
            return False

    def make_temp_distribution(self):
        # Create series of numbers between Temp_Min and Temp_Max
        step = (self.Temp_Max - self.Temp_Min) / (self.SERIES_DENSITY - 1)
        series = [self.Temp_Min + i * step for i in range(self.SERIES_DENSITY)]

        # Return the series of temperatures (uniform sampling for now)
        return series

    def increment_day(self):
        self.day += 1

    def daily_stats(self, temperature):
        print("You have $" + str(self.cash) + " cash on hand and the temperature is " + str(temperature) + ".")
        print("You have enough coffee on hand to make " + str(self.coffee_inventory) + " cups \n")

    def day_header(self):
        print("\n-----| Day " + str(self.day) + "@" + self.shop_name + " |-----\n")

    def daily_sales(self, temperature, advertising, cup_price):
        # Randomize advertising effectiveness
        adv_coefficient = random.randint(20, 80) / 100

        # Higher priced coffee doesn't sell as well
        price_coefficient = int((cup_price * (random.randint(50, 250) / 100)))

        # Run the sales figures!
        sales = int((self.Temp_Max - temperature) * (advertising * adv_coefficient))

        # If price is too high, we don't sell anything
        if price_coefficient > sales:
            sales = 0
        else:
            sales -= price_coefficient

        if sales > self.coffee_inventory:
            sales = self.coffee_inventory
            print("You would have sold more coffee but you ran out. Be sure to buy additional inventory.")

        return sales

    @property
    def weather(self):
        # Generate a random temperature between Temp_Min and Temp_Max
        return int(random.choice(self.temps))

    @staticmethod
    def prompt(display="Please input a string", require=True):
        if require:
            s = False
            while not s:
                s = input(display + " ")
        else:
            s = input(display + " ")
        return s

    @staticmethod
    def x_of_y(x, y):
        num_list = []
        # return a list of x numbers of y
        for i in range(x):
            num_list.append(y)
        return num_list

    @staticmethod
    def convert_to_float(value):
        try:
            if value is None or value == "":
                return 0.0
            return float(value)
        except (ValueError, TypeError):
            return 0.0