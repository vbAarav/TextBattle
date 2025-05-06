import magic.sigils as sigils
import time
import math
import random
from enum import Enum, auto

# Character Class
class Character:
    def __init__(self, name, max_hp, attack, defense, speed, race=None,
                resistance=0, crit_chance=0.1, crit_resistance=0, crit_damage=1.5,
                crit_shield=0, evasion=0, accuracy=0.9, type=None, sigils=None, status_effects=None, description=""):
        # Description
        self.name = name
        self.description = description
        self.race = race

        # Properties
        self.type = Colour.NONE if type is None else type

        # Stats
        self.max_hp = ResourceStat(max_hp, name="MAXHP")
        self.attack = Stat(attack, name="ATK")
        self.speed = Stat(speed, name="SPD")
        self.defense = Stat(defense, name="DEF")

        # Complex Stats
        self.resistance = Stat(resistance, name="RES", is_natural=False)
        self.crit_chance = Stat(crit_chance, name="CC", is_float=True)
        self.crit_resistance = Stat(crit_resistance, name="CR", is_float=True)
        self.crit_damage = Stat(crit_damage, name="CD", is_float=True)
        self.crit_shield = Stat(crit_shield, name="CS", is_float=True)

        self.evasion = Stat(evasion, name="EV", is_float=True)
        self.accuracy = Stat(accuracy, name="ACC", is_float=True)
        
        # Battle Stats
        self.action_points = Stat(0, name="AP", is_float=0)

        # States
        self.acts = True

        # Belongings
        self.items = []
        self.sigils = sigils if sigils is not None else []
        for sigil in self.sigils:
            sigil.equipped_character = self

        # Status Effects
        self.status_effects = status_effects if status_effects is not None else []

    def __repr__(self):
        toReturn = f"{self.name} [{self.type}](HP: {self.max_hp.resource_value}/{self.max_hp.total}, ATK: {self.attack.total}, DEF: {self.defense.total}, SPD: {self.speed.total})"

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
    
    def display_details(self):
        print(f"{self.name}")
        if self.description != "":
            print(f"    {self.description}")
        print(f"    Type: {self.type}")
        print(f"    HP: {self.max_hp.resource_value}/{self.max_hp.total}")
        print(f"    ATK: {self.attack.total}")
        print(f"    DEF: {self.defense.total}")
        print(f"    SPD: {self.speed.total}")
        print(f"    RES: {self.resistance.total}")
        print(f"    CC: {self.crit_chance.total * 100:.0f}%")
        print(f"    CR: {self.crit_resistance.total * 100:.0f}%")
        print(f"    CD: {self.crit_damage.total * 100:.0f}%")
        print(f"    CS: {self.crit_shield.total * 100:.0f}%")
        print(f"    EV: {self.evasion.total * 100:.0f}%")
        print(f"    ACC: {self.accuracy.total * 100:.0f}%")

        print(f"\nSigils:")
        for sigil in self.sigils:
            print(f"    {sigil.name}", end="")
            if sigil.description != "":
                print(f" - {sigil.description}", end="")
            print("")
            for effect in sigil.active_effects:
                print(f"        (Active) {effect.name} - {effect.description}")
            for effect in sigil.passive_effects:
                print(f"        (Passive) {effect.name} - {effect.description}")
        
        print("")


    # Character State Methods
    def is_alive(self):
        return self.max_hp.resource_value > 0
    
    def can_act(self):
        return self.acts

    def all_stats(self):
        return [self.max_hp, self.attack, self.defense, self.speed, self.resistance, self.crit_chance, self.crit_resistance, self.crit_damage, self.crit_shield, self.evasion, self.accuracy]

    # Character Property Manipulation Methods
    def receive_attack(self, incoming_damage, attacker, battle):
        # Trigger passive effects before receiving an attack
        battle.trigger_effects(self, trigger="after_receive_attack", attacker=attacker)
        time.sleep(1)
        
        # Calculate if attack connects with target       
        chance_to_hit = attacker.accuracy.total - self.evasion.total 
        if (random.random() <= chance_to_hit): 
            # Calculate the damage received
            incoming_damage.crit_amount -= self.crit_shield.total  
            reduction = (incoming_damage.ignore_defense * self.defense.total) * ((self.resistance.total/100) + 1)  # Calculate Resistance
            amount_damage = int(math.floor(max(0, incoming_damage.total - reduction)))  # Total Damage

            if incoming_damage.is_crit:
                print(f"CRITICAL HIT!!!")
                time.sleep(1)

            # Character Takes Damage
            self.take_damage(amount_damage, battle, source=attacker)
            time.sleep(1)

            # Trigger passive effects after receiving an attack
            battle.trigger_effects(self, trigger="after_receive_attack", attacker=attacker)
            time.sleep(1)
        else:
            print(f"{attacker.name} missed the attack")
            time.sleep(1)

    def attack_target(self, target, battle):
        print(f"{self.name} attacks {target.name}!")
        time.sleep(1)
        
        # Trigger passive effects before performing an attack
        battle.trigger_effects(self, trigger="before_attack", target=target)
        time.sleep(1)

        # Calculate Damage
        damage = Damage()
        damage.build(self.attack.total, self, target)
        target.receive_attack(damage, self, battle)

        # Trigger passive effects after performing an attack
        battle.trigger_effects(self, trigger="after_attack", target=target)
        time.sleep(1)

    def receive_heal(self, heal_amount):
        self.max_hp.change_resource_by_val(heal_amount)
        print(
            f"{self.name} heals for {heal_amount} HP. HP: {self.max_hp.resource_value}")
        time.sleep(1)

    def add_status_effect(self, status_effect, battle):
        if status_effect not in self.status_effects:
            status_effect.current_stack += 1
            self.status_effects.append(status_effect)
            status_effect.on_apply(self, battle)
            print(f"{self.name} is now affected by {status_effect.name}.")
            time.sleep(1)

    def clear_stat_modifiers(self):
        for stat in self.all_stats():
            stat.clear_modifiers()

    def equip_sigil(self, sigil):
        self.sigils.append(sigil)
        sigil.equipped_character = self

    # Sigil Methods
    def activate_active_effect(self, sigil, effect, battle):
        if sigil in self.sigils:
            if effect in sigil.active_effects:
                effect.apply(self, battle)

    # Stat Changes
    def take_damage(self, damage, battle, source=None):
        old_hp = self.max_hp.resource_value
        self.max_hp.change_resource_by_val(-damage)
        print(
            f"{self.name} takes {damage} damage! HP: {old_hp} --> {self.max_hp.resource_value}")

        if self.max_hp.resource_value <= 0:
            self.on_death(battle, source=source)

    def on_death(self, battle, source=None):
        # Trigger passive effects when dying by an ally or enemy
        trigger_type = "on_death_by_ally" if source in battle.get_character_allies(
            self) else "on_death_by_enemy"
        battle.trigger_effects(self, trigger=trigger_type, killer=source)

# Damage
class Damage:
    def __init__(self, amount=0, crit_amount=0, is_crit=False, type_amount=0, has_advantage=False, has_disadvantage=False):
        self.base_amount = amount
        self.crit_amount = crit_amount
        self.is_crit = is_crit
        self.type_amount = type_amount
        self.has_advantage = has_advantage
        self.has_disadvantage = has_disadvantage
        self.ignore_defense = 1

    def build(self, amount, attacker, target):
        self.base_amount = amount
        self.is_crit = random.random() <= (
            attacker.crit_chance.total - target.crit_resistance.total)
        self.crit_amount = attacker.crit_damage.total
        self.has_advantage = attacker.type.has_advantage(target.type)
        self.has_disadvantage = attacker.type.has_disadvantage(target.type)
        self.type_amount = 0.5 if self.has_disadvantage else (
            1.5 if self.has_advantage else 1)

    @property
    def total(self):
        total = (self.base_amount + random.uniform(0, (math.log10(self.base_amount) + 1)* 10)) * self.type_amount * self.crit_amount
        return int(math.floor(total))

# Stats
class Stat:
    def __init__(self, base_value, name=None, is_natural=True, is_float=False):
        self.name = None if name is None else name
        self.base_value = base_value
        self.additive_modifiers = []  # Flat increases/decreases
        self.multiplicative_modifiers = []  # Percentage-based increases

        self.is_natural = is_natural
        self.is_float = is_float

    def add_modifier(self, value: float, is_multiplicative: bool = False):
        """Adds a modifier. Set is_multiplicative=True for percentage-based modifiers."""
        if is_multiplicative:
            self.multiplicative_modifiers.append(value)
        else:
            self.additive_modifiers.append(value)

    def remove_modifier(self, value: float, is_multiplicative: bool = False):
        """Removes a modifier if it exists."""
        if is_multiplicative and value in self.multiplicative_modifiers:
            self.multiplicative_modifiers.remove(value)
        elif value in self.additive_modifiers:
            self.additive_modifiers.remove(value)
        

    def clear_modifiers(self):
        """Clears all modifiers."""
        self.additive_modifiers.clear()
        self.multiplicative_modifiers.clear()

    @property
    def total(self):
        """Calculates the total stat value with all modifiers applied."""
        total_value = self.base_value + sum(self.additive_modifiers)
        for multiplier in self.multiplicative_modifiers:
            total_value = total_value * multiplier
        if self.is_natural:
            total_value = max(0, total_value)  # Ensure non-negative stats
        if not self.is_float:
            total_value = int(total_value)
        return total_value

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

# Colour Type
class Colour(Enum):
    NONE = auto()
    RED = auto()
    BLUE = auto()
    GREEN = auto()
    PURPLE = auto()
    YELLOW = auto()

    def random_type():
        return random.choice((Colour.RED, Colour.BLUE, Colour.GREEN, Colour.PURPLE, Colour.YELLOW))

    # Has Advantage
    def has_advantage(self, other):
        if self == Colour.RED and other == Colour.GREEN:
            return True
        if self == Colour.BLUE and other == Colour.RED:
            return True
        if self == Colour.GREEN and other == Colour.BLUE:
            return True
        if self == Colour.PURPLE and other == Colour.PURPLE:
            return True
        if self == Colour.YELLOW and other == Colour.YELLOW:
            return True
        return False

    # Has Disadvantage
    def has_disadvantage(self, other):
        if self == Colour.RED and other == Colour.BLUE:
            return True
        if self == Colour.BLUE and other == Colour.GREEN:
            return True
        if self == Colour.GREEN and other == Colour.RED:
            return True
        return False

    def __str__(self):
        if self == Colour.NONE:
            return "NON"
        if self == Colour.RED:
            return "RED"
        if self == Colour.BLUE:
            return "BLU"
        if self == Colour.GREEN:
            return "GRN"
        if self == Colour.YELLOW:
            return "YLW"
        if self == Colour.PURPLE:
            return "PUR"
