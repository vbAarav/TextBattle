import random
import time

# Effect Classes
class Effect:
    def __init__(self, name, description=""):
        self.name = name
        self.description = description

    def apply(self, character, battle):
        # General method to apply an effect
        raise NotImplementedError(
            "Subclasses must implement the 'apply' method.")

    def __repr__(self):
        return f"Effect({self.name})"


class ActiveEffect(Effect):
    def __init__(self, name, description="", effect_function=None):
        super().__init__(name, description)
        self.effect_function = effect_function  # Function to apply the active effect

    def apply(self, character, battle):
        if self.effect_function:
            self.effect_function(character, battle)

    def __repr__(self):
        return f"ActiveEffect({self.name})"


class PassiveEffect(Effect):
    def __init__(self, name, description="", effect_function=None, trigger_condition=None):
        super().__init__(name, description)
        self.effect_function = effect_function  # Function to apply the passive effect
        self.trigger_condition = trigger_condition

    def check_and_apply(self, character, battle, **kwargs):
        """Checks if the condition is met and applies the effect if so."""
        if self.trigger_condition and self.trigger_condition(character, battle, **kwargs):
            print(f"{character.name}'s {self.name} is triggered.")
            time.sleep(1)
            self.apply(character, battle)

    def apply(self, character, battle):
        # Passive effects may be triggered on certain events automatically
        if self.effect_function:
            self.effect_function(character, battle)

    def __repr__(self):
        return f"PassiveEffect({self.name})"

class StatusEffect(Effect):
    def __init__(self, name, description="", duration=1, apply_effect=None, ongoing_effect=None, trigger_condition=None):
        super().__init__(name, description)
        self.duration = duration
        self.apply_effect = apply_effect
        self.ongoing_effect = ongoing_effect    
        self.trigger_condition = trigger_condition
        
    def check_and_apply(self, character, battle, **kwargs):
        """Checks if the condition is met and applies the effect if so."""
        if self.trigger_condition and self.trigger_condition(character, battle, **kwargs):
            self.apply(character, battle)

    def apply(self, character, battle):
        if self.apply_effect:
            self.apply_effect(character, battle)
        
    def update_effect(self, character, battle, **kwargs):
        if self.ongoing_effect:
            if self.trigger_condition and self.trigger_condition(character, battle, **kwargs):
                self.ongoing_effect(character, battle)
        self.decrement_duration(character)
        
    def decrement_duration(self, character):
        self.duration -= 1
        if self.duration <= 0:  
            character.status_effects.remove(self)
            print(f"{character.name} is no longer affected by {self.name}.")
        

    def __repr__(self):
        return f"{self.name}: {self.duration}"






















# Trigger Conditions
def trigger_on_start_of_battle(character, battle, **kwargs):
    return kwargs.get("trigger") == "on_start_of_battle"

def trigger_on_start_of_turn(character, battle, **kwargs):
    return kwargs.get("trigger") == "on_start_of_turn"


def trigger_on_receive_attack(character, battle, **kwargs):
    return kwargs.get("trigger") == "on_receive_attack"


def trigger_on_attack(character, battle, **kwargs):
    return kwargs.get("trigger") == "on_attack"


def trigger_on_turn_x(x):
    return lambda character, battle, **kwargs: kwargs.get("trigger") == "on_turn" and kwargs.get("turn") == x


def trigger_within_first_x_turns(x):
    return lambda character, battle, **kwargs: kwargs.get("trigger") == "on_turn" and kwargs.get("turn") <= x


def trigger_on_death_by_ally(character, battle, **kwargs):
    return kwargs.get("trigger") == "on_death_by_ally"


def trigger_on_death_by_enemy(character, battle, **kwargs):
    return kwargs.get("trigger") == "on_death_by_enemy"


def trigger_on_stat_threshold(stat, condition):
    return lambda character, battle, **kwargs: condition(getattr(character, stat), character)


def trigger_if_ally_present(name):
    return lambda character, battle, **kwargs: any(ally.name == name for ally in battle.get_character_allies(character))







# Active Effects
def large_slice(character, battle):
    target = battle.choose_target(battle.get_all_characters(), character)
    if target:
        print(f"{character.name} attacks {target.name}!")
        multiplier = random.uniform(1.0, 1.5)
        damage = max(character.attack + 1, int(character.attack * multiplier))
        target.receive_attack(damage, character, battle)
        time.sleep(1)


def heal_all_allies(character, battle):
    for ally in battle.get_character_allies(character):
        heal_amount = ally.max_hp * 0.5
        ally.receive_heal(heal_amount)
        time.sleep(1)


def swap_atk_def(character, battle):
    character.attack, character.defense = character.defense, character.attack
    print(f"{character.name} swapped ATK and DEF stats.")
    time.sleep(1)


def damage_ally_and_poison_enemy(character, battle):
    target = battle.choose_target(battle.get_all_characters(), character)
    if (target in battle.get_character_allies(character)) and (target != character):
        # Deal Damage
        print(f"{character.name} attacks {target.name}!")
        damage = max(character.attack + 1, int(character.attack * 1.8))
        target.receive_attack(damage, character, battle)

        # Poison
        random_enemy = random.choice(battle.get_character_enemies(character))
        random_enemy.add_status_effect(effect_status_poison)

    else:
        # Deal Damage
        print(f"{character.name} attacks {target.name}!")
        damage = int(character.attack * 0.5)
        target.receive_attack(damage, character, battle)



# Passive Effects
def thousand_divine_cuts(character, battle):
    for enemy in battle.get_character_enemies(character):
        old_defense = enemy.defense
        enemy.defense = min(enemy.defense - 1, int(enemy.defense * 0.95))
        print(f"{enemy.name} DEF reduced by 5% {old_defense} -> {enemy.defense}")


def early_stance(character, battle):
    old_defense = character.defense
    character.defense = max(character.defense + 1, int(character.defense * 1.2))
    print(f"{character.name} enters an early stance. DEF increased by 20%. {old_defense} -> {character.defense}")


def engine(character, battle):
    old_speed = character.speed
    character.speed += 1
    print(f"{character.name} SPD increased by 1. {old_speed} -> {character.speed}")


def double_up(character, battle):
    old_attack = character.attack
    character.attack = max(character.attack + 1, int(character.attack * 1.01))
    print(f"{character.name} ATK increased by 1%. {old_attack} -> {character.attack}")


def late_bloomer(character, battle):
    character.hp = character.max_hp
    print(f"{character.name} fully recovers HP.")


def last_stance(character, battle):
    old_attack = character.attack
    character.attack = max(character.attack + 1, int(character.attack * 1.5))
    print(f"{character.name} ATK increased by 50%. {old_attack} -> {character.attack}")


def wolf_hunger(character, battle):
    for ally in battle.get_character_allies(character):
        old_attack = ally.attack
        ally.attack = max(ally.attack + 1, int(ally.attack * 1.5))
        print(f"{ally.name} ATK increased by 50%. {old_attack} -> {ally.attack}")
        
        
        
# Status Effects
def poison(character, battle):
    damage = character.max_hp * 0.06
    print(f"{character.name} is poisoned")
    character.take_damage(damage, battle)
    


# Create A Large Set of Effects

# Active Effects
effect_large_slice = ActiveEffect(
    "Large Slice", description="Attacks the target. Dealing (100% - 150%) of ATK as Damage", effect_function=large_slice)
effect_heal_all = ActiveEffect(
    "Heal All", description="All allies heal health equal to 50% of MAXHP", effect_function=heal_all_allies)
effect_guard_switch = ActiveEffect(
    "Guard Switch", description="Swaps the character's ATK and DEF Stats", effect_function=swap_atk_def)
effect_enforced_vigor = ActiveEffect(
    "Enforced Vigor", description="Attacks the target. Dealing 50% of ATK as Damage. If the target is an ally. Attacks the target. Dealing 180% of ATK as Damage and poison a random enemy for 3 turns.", effect_function=damage_ally_and_poison_enemy)

# Passive Effects
effect_thousand_divine_cuts = PassiveEffect("Thousand Divine Cuts", description="At the start of battle, All enemies have DEF reduced by 5%", 
                            effect_function=thousand_divine_cuts, trigger_condition=trigger_on_start_of_battle)

effect_engine = PassiveEffect("Engine", description="After receiving an attack, SPD + 1",
                              effect_function=engine, trigger_condition=trigger_on_receive_attack)

effect_double_up = PassiveEffect("Double Up", description="After executing an attack, Increase ATK by 1%",
                                 effect_function=double_up, trigger_condition=trigger_on_attack)

effect_late_bloomer = PassiveEffect("Late Bloomer", description="On Turn 2, Fully recover HP",
                                    effect_function=late_bloomer, trigger_condition=trigger_on_turn_x(2))

effect_early_stance = PassiveEffect("Early Stance", description="For 5 turns, Increase DEF by 20%",
                                    effect_function=early_stance, trigger_condition=trigger_within_first_x_turns(5))

effect_last_stance = PassiveEffect("Last Stance", description="When HP is below 50%. Increase ATK by 50%", effect_function=last_stance,
                                   trigger_condition=trigger_on_stat_threshold("hp", lambda hp, character: hp < character.max_hp / 2))

effect_wolf_hunger = PassiveEffect("Wolf Hunger", description="When killed by an enemy. Increase allies ATK by 50%",
                                   effect_function=wolf_hunger, trigger_condition=trigger_on_death_by_enemy)

# Status Effects
effect_status_poison = StatusEffect("Poison", description="Takes 6% of Max HP as damage at the start of turn", duration=3, ongoing_effect=poison, trigger_condition=trigger_on_start_of_turn)


