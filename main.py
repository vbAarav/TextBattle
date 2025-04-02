
import time
import character.characters as characters
import magic.sigils as sigils
import players
import map.location as location
import map.area_atlus as area_atlus
import character.character_archive as character_archive
import magic.sigil_archive as sigil_archive


def play_intro():
    print("One day, the world was plagued by a strange phenomenon that stretched across the world.")
    time.sleep(2)
    print("A new force that influenced our universe was discovered.")
    time.sleep(2)
    print("The supernatural. It affected many things in our world. ")
    time.sleep(2)
    print("It had a major influence on the bio ecosystem.")
    time.sleep(2)
    print("The animals and plants went through a drastic change.")
    time.sleep(2)
    print("And the world was blessed with new resources")
    time.sleep(2)
    print("Strange new minerals and plants were discovered.")
    time.sleep(2)
    print("Which could be used in medicine and technology.")
    time.sleep(2)
    print("Some people were given gifts.")
    time.sleep(2)
    print("They could do extraordinary things.")
    time.sleep(2)
    print("Some could control fire.")
    time.sleep(2)
    print("Some could levitate objects.")
    time.sleep(2)
    print("Some could even teleport.")
    time.sleep(2)
    print("The world was in awe.")
    time.sleep(2)
    print("But it also brought forth new dangers.")
    time.sleep(2)
    print("Sharks could fly and attack people on the beaches.")
    time.sleep(2)
    print("Bees could use telekinesis and sting their prey.")
    time.sleep(2)
    print("Spoons would transform into monsters and attack civilians.")
    time.sleep(2)
    print("The world was entering a chaotic era.")
    time.sleep(2)
    print("However, humanity was prepared.")
    time.sleep(2)
    print("The supernatural influenced both the good and the bad.")
    time.sleep(2)
    print("And so, the world was able to handle these new threats.")
    time.sleep(2)
    print("But the chaos never stopped.")
    time.sleep(2)
    print("And so, the world was trapped in a never-ending cycle.")
    time.sleep(2)


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

        choice = self.player.get_input(
            "Choose an action: ", ["1", "2", "3", "4", "5"])

        if choice == "1":
            new_location = self.map.find_new_location(
                self.player, self.player.location)
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
# play_intro()


name = input("What is your name: ")
player = players.Player(name, location=area_atlus.LONG_PLAINS)

# Build Character Team
name = input("What is your character's name: ")
character = character_archive.MC_TEMPLATE
character.name = name
character.type = characters.Colour.random_type()
character = characters.Character(name, max_hp=100, attack=3, defense=1, speed=1, type=characters.Colour.random_type(), sigils=[sigil_archive.POWER])
player.characters.append(character)

print("Choose a team member to join you")
ipt = input("1. Azelgram\n")
player.characters.append(character_archive.AZELGRAM)

# Game Loop
print(f"{character.name} has entered the world!\n")
time.sleep(1)
game = Game(player)
game.start_game()
