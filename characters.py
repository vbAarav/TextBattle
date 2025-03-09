import runes
import time

class Character:
    def __init__(self, name, max_hp, attack, defense, speed, runes=None, status_effects=None, description=""):
        # Stats
        self.name = name
        self.max_hp = max_hp
        self.hp = self.max_hp
        self.attack = attack
        self.speed = speed
        self.defense = defense
        
        # Description
        self.description = description

        # Runes
        self.runes = runes if runes is not None else []
        for rune in self.runes:
            rune.equipped_character = self

        # Status Effects 
        self.status_effects = status_effects if status_effects is not None else []

        
    def __repr__(self):
        toReturn = f"{self.name} (HP: {self.hp}/{self.max_hp}, ATK: {self.attack}, DEF: {self.defense}, SPD: {self.speed})"
        if len(self.status_effects) > 0:
            toReturn += f" Statuses: {self.status_effects}"
        return toReturn
        
    def equip_rune(self, rune):
        self.runes.append(rune)
        rune.equipped_character = self
        
    # Character State Methods
    def is_alive(self):
        return self.hp > 0

    # Character Property Manipulation Methods
    def receive_attack(self, incoming_damage, attacker, battle):
        damage = max(0, incoming_damage - self.defense)
        self.take_damage(damage, battle, source=attacker)
        time.sleep(1)

        # Trigger passive effects after receiving an attack
        battle.trigger_effects(self, trigger="on_receive_attack", attacker=attacker)
        time.sleep(1)
        

    def attack_target(self, target, battle):
        print(f"{self.name} attacks {target.name}!")
        time.sleep(1)
        target.receive_attack(self.attack, self, battle)
        
        # Trigger passive effects when performing an attack
        battle.trigger_effects(self, trigger="on_attack", target=target)
        time.sleep(1)

    
    def receive_heal(self, heal_amount):
        self.hp = min(self.hp + heal_amount, self.max_hp)
        print(f"{self.name} heals for {heal_amount} HP. HP: {self.hp}")
        time.sleep(1)
        
    def add_status_effect(self, status_effect):
        if status_effect not in self.status_effects:
            self.status_effects.append(status_effect)
            print(f"{self.name} is now affected by {status_effect.name}.")
            time.sleep(1)
        
    # Rune Methods
    def activate_active_effect(self, rune, effect, battle):
        if rune in self.runes:
            if effect in rune.active_effects:
                effect.apply(self, battle)
                
    # Stat Changes
    def take_damage(self, damage, battle, source=None):
        old_hp = self.hp
        self.hp = max(0, self.hp - damage)
        print(f"{self.name} takes {damage} damage! HP: {old_hp} --> {self.hp}")
        
        if self.hp == 0:
            self.on_death(battle, source=source)
                
    def on_death(self, battle, source=None):
        # Trigger passive effects when dying by an ally or enemy
        trigger_type = "on_death_by_ally" if source in battle.get_character_allies(self) else "on_death_by_enemy"
        battle.trigger_effects(self, trigger=trigger_type, killer=source)
                

    
    

    