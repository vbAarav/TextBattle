import time
import random


class Player:
    def __init__(self, name, characters=None, location=None, inventory=None):
        self.characters = [] if characters is None else characters
        self.name = name
        self.location = location
        self.inventory = [] if inventory is None else inventory

    def __repr__(self):
        toReturn = f"{self.name}"
        return toReturn
    
    def get_input(self, message, valid_choices):
        choice = input(message).strip()
        while choice not in valid_choices:
            print("Invalid input!")
            time.sleep(1)
            choice = input(message).strip()
        return choice

    def travel_to(self, location):
        self.location = location    

    def add_inventory_item(self, item):
        self.inventory.append(item)

    def add_inventory_loot(self, loot):
        self.inventory.extend(loot)


class Enemy(Player):
    def __init__(self, characters=None):
        self.rewards = {}
        super().__init__("Enemy", characters)

    def get_input(self, message, valid_choices):
        choice = random.choices(valid_choices, weights=[int(choice) ** 2 for choice in valid_choices], k=1)[0]
        time.sleep(1)
        return choice

    def generate_rewards(self):
        pass
