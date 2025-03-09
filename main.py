import random
import characters
import battle
import runes
import effects
import players

# Create Players
player = players.Player("The Player")
enemy = players.Enemy()

player.characters = [characters.chr_warrior, characters.chr_undead_soldier]
enemy.characters = [characters.chr_orc, characters.chr_goblin]

b = battle.Battle(player, enemy)
b.start_battle()
