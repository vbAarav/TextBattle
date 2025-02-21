import random
import characters
import battle

# Example characters
team1 = [characters.Character("Hero", hp=30, attack=8, defense=4, speed=10), characters.Character("Warrior", hp=40, attack=10, defense=4, speed=7)]
team2 = [characters.Character("Goblin", hp=20, attack=6, defense=4, speed=5), characters.Character("Orc", hp=35, attack=9, defense=4, speed=6)]

b = battle.Battle(team1, team2)
b.start_battle()
