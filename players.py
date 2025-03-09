import time
import random

class Player:
    def __init__(self, name, characters=None):
        self.characters = characters if characters is None else characters
        self.name = name
        
    def get_input(self, message, valid_choices):
        choice = input(message).strip()
        while choice not in valid_choices:
            print("Invalid input!")
            time.sleep(1)
            choice = input(message).strip()
        return choice
    
class Enemy(Player):
    def __init__(self):
        super().__init__("Enemy")
        
    def get_input(self, message, valid_choices):
        choice = random.choice(valid_choices)
        time.sleep(1)
        return choice
        
        