import runes
class Character:
    def __init__(self, name, max_hp, attack, defense, speed, runes=[]):
        # Stats
        self.name = name
        self.max_hp = max_hp
        self.hp = self.max_hp
        self.attack = attack
        self.speed = speed
        self.defense = defense
        
        # Runes
        self.runes = runes
        for rune in self.runes:
            rune.equipped_character = self
        
    def equip_rune(self, rune):
        self.runes.append(rune)
        rune.equipped_character = self
        
    # Is the Character Alive
    def is_alive(self):
        return self.hp > 0

    # Attack Methods
    def receive_attack(self, damage):
        self.hp = max(0, self.hp - (damage - self.defense))
        print(f"{self.name} takes {damage} damage! HP: {self.hp}")

    def attack_target(self, target):
        print(f"{self.name} attacks {target.name}!")
        target.receive_attack(self.attack)
        
    # Heal Methods
    def receive_heal(self, heal_amount):
        self.hp = min(self.hp + heal_amount, self.max_hp)
        print(f"{self.name} heals for {heal_amount} HP. HP: {self.hp}")
        
    # Rune Methods
    def activate_active_effect(self, rune, effect, battle):
        if rune in self.runes:
            if effect in rune.active_effects:
                effect.apply(self, battle)
    
    def apply_passive_effects(self, rune):
        for rune in self.runes:
            for effect in rune.passive_effects:
                effect.apply(self)
                
# List of Characters
chr_warrior = Character("Warrior", max_hp=100, attack=10, defense=1, speed=20, runes=[runes.power_rune, runes.crystalised_ice_rune])
chr_undead_soldier = Character("Undead Soldier", max_hp=150, attack=4, defense=7, speed=5, runes=[runes.glowing_grass_rune])
chr_orc = Character("Orc", max_hp=100, attack=9, defense=4, speed=6)
chr_goblin = Character("Goblin", max_hp=100, attack=6, defense=4, speed=5)
    
    

    