
import time
import character.characters as characters
import magic.sigils as sigils
import players
import map.location as location
import map.area_atlus as area_atlus
import character.character_archive as character_archive
import magic.sigil_archive as sigil_archive

class Game:
    def __init__(self, player):
        self.player = player
        self.map = location.Map()
        self.map.add_area(self.player.location)

    def start_game(self):
        print(f"You have entered the {self.player.location}.")
        self.in_world()

    def in_world(self):
        print("\nWhat would you like to do:")
        print("1. Travel To New Location")
        print("2. Explore Area")
        print("3. View Characters")
        print("4. View Inventory")
        print("5. Quit")

        choice = self.player.get_input("Choose an action: ", ["1", "2", "3", "4", "5"])

        if choice == "1":
            new_location = self.map.find_new_location(self.player, self.player.location)
            while new_location is None:
                new_location = self.map.find_new_location(
                    self.player, self.player.location)
            self.player.travel_to(new_location)
            self.in_world()

        elif choice == "2":
            player.location.explore_area(player)
            self.in_world()

        elif choice == "3":
            self.player.view_characters()
            self.in_world()

        elif choice == "4":
            self.player.view_inventory()
            self.in_world()
        elif choice == "5":
            print("Thanks for playing!")
        else:
            return False
        

# Start of the Game
name = input("What is your name: ")
player = players.Player(name, location=area_atlus.LONG_PLAINS)

# Build Character Team
name = input("What is your character's name: ")
character = character_archive.MC_TEMPLATE
character.name = name
character.type = characters.Colour.random_type()
character = characters.Character(name, max_hp=100, attack=11, defense=1, speed=1, type=characters.Colour.random_type(), sigils=[sigil_archive.GRIM_CORPSE])
player.characters.append(character)


# Game Loop
print(f"{character.name} has entered the world!\n")
time.sleep(1)
game = Game(player)
game.start_game()
