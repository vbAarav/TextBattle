import runes
import time

class Character:
    def __init__(self, name, max_hp, attack, defense, speed, runes=None, status_effects=None, description=""):
        # Description
        self.name = name
        self.description = description
        
        # Stats
        self.max_hp = ResourceStat(max_hp, name="MAXHP")
        self.attack = Stat(attack, name="ATK")
        self.speed = Stat(speed, name="SPD")
        self.defense = Stat(defense, name="DEF")      

        # Belongings
        self.items = []
        self.runes = runes if runes is not None else []
        for rune in self.runes:
            rune.equipped_character = self

        # Status Effects 
        self.status_effects = status_effects if status_effects is not None else []

        
    def __repr__(self):
        toReturn = f"{self.name} (HP: {self.max_hp.resource_value}/{self.max_hp.total}, ATK: {self.attack.total}, DEF: {self.defense.total}, SPD: {self.speed.total})"
        
        # Additive
        for stat in [self.max_hp, self.attack, self.defense, self.speed]:
            if stat.additive_modifiers:
                toReturn += f" {stat.name} {'+' if sum(stat.additive_modifiers) >= 0 else '-'}{sum(stat.additive_modifiers)}"
   
        # Multiply
        for stat in [self.max_hp, self.attack, self.defense, self.speed]:
            for modifier in stat.multiplicative_modifiers:
                toReturn += f" {stat.name} {'+' if (modifier - 1) >= 0 else ''}{(modifier - 1) * 100:.0f}%"      
                              
        # Statuses
        if len(self.status_effects) > 0:
            toReturn += f" Statuses: {self.status_effects}"
        return toReturn
        
    def equip_rune(self, rune):
        self.runes.append(rune)
        rune.equipped_character = self
        
    # Character State Methods
    def is_alive(self):
        return self.max_hp.resource_value > 0

    # Character Property Manipulation Methods
    def receive_attack(self, incoming_damage, attacker, battle):
        damage = max(0, incoming_damage - self.defense.total)
        self.take_damage(damage, battle, source=attacker)
        time.sleep(1)

        # Trigger passive effects after receiving an attack
        battle.trigger_effects(self, trigger="on_receive_attack", attacker=attacker)
        time.sleep(1)
        

    def attack_target(self, target, battle):
        print(f"{self.name} attacks {target.name}!")
        time.sleep(1)
        target.receive_attack(self.attack.total, self, battle)
        
        # Trigger passive effects when performing an attack
        battle.trigger_effects(self, trigger="on_attack", target=target)
        time.sleep(1)
    
    def receive_heal(self, heal_amount):
        self.max_hp.change_resource_by_val(heal_amount)
        print(f"{self.name} heals for {heal_amount} HP. HP: {self.max_hp.resource_value}")
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
        old_hp = self.max_hp.resource_value
        self.max_hp.change_resource_by_val(-damage) 
        print(f"{self.name} takes {damage} damage! HP: {old_hp} --> {self.max_hp.resource_value}")
        
        if self.max_hp.resource_value <= 0:
            self.on_death(battle, source=source)
                
    def on_death(self, battle, source=None):
        # Trigger passive effects when dying by an ally or enemy
        trigger_type = "on_death_by_ally" if source in battle.get_character_allies(self) else "on_death_by_enemy"
        battle.trigger_effects(self, trigger=trigger_type, killer=source)
   

# Stats    
class Stat:
    def __init__(self, base_value, name=None):
        self.name = None if name is None else name
        self.base_value = base_value
        self.additive_modifiers = []  # Flat increases/decreases
        self.multiplicative_modifiers = []  # Percentage-based increases

    def add_modifier(self, value: float, is_multiplicative: bool = False):
        """Adds a modifier. Set is_multiplicative=True for percentage-based modifiers."""
        if is_multiplicative:
            self.multiplicative_modifiers.append(value)
        else:
            self.additive_modifiers.append(value)

    def remove_modifier(self, value: float):
        """Removes a modifier if it exists."""
        if value in self.additive_modifiers:
            self.additive_modifiers.remove(value)
        elif value in self.multiplicative_modifiers:
            self.multiplicative_modifiers.remove(value)

    @property
    def total(self):
        """Calculates the total stat value with all modifiers applied."""
        total_value = self.base_value + sum(self.additive_modifiers)
        for multiplier in self.multiplicative_modifiers:
            total_value = total_value * multiplier
        return max(0, int(total_value))  # Ensure non-negative stats                                                    

    def __repr__(self):
        return f"Stat(base={self.base_value}, total={self.total})"
    
    
# Resource Stat
class ResourceStat(Stat):
    def __init__(self, max_value, name=None):
        super().__init__(max_value, name)
        self.resource_value = self.total
        
    def change_resource_by_val(self, val):
        self.resource_value = min(self.total, max(self.resource_value + val, 0))
    
    def change_resource_by_perc(self, val):
        self.resource_value = max(0, max(self.total, int((self.get_percentage() + val) * self.total)))
        
    def get_percentage(self):
        return (self.resource_value/self.total)
        
    def __repr__(self):
        return f"Stat(base={self.resource_value}/{self.base_value}, total={self.resource_value}/{self.total})"

                

    
    

    