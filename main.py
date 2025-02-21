import random
import characters
import battle
import runes
import effects

b = battle.Battle([characters.chr_warrior, characters.chr_undead_soldier], [characters.chr_orc, characters.chr_goblin])
b.start_battle()
