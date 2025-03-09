import random
import time
import characters
import battle
import runes
import effects
import players
import data


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

# Start of the Game
play_intro()

name = input("What is your name: ")
player = players.Player(name)

# Choose a character
print("Which character would you like to play as?")



