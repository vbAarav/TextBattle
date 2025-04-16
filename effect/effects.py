import random
import time                                 
class ActiveEffect:
    def __init__(self, name, description="", effect_function=None):
        self.name = name
        self.description = description
        self.effect_function = effect_function  # Function to apply the active effect

    def apply(self, character, battle):
        if self.effect_function:
            self.effect_function(character, battle)

    def __repr__(self):
        return f"ActiveEffect({self.name})"
    
class ComplexEffect:
    def __init__(self, trigger, effect,
                 condition=None,
                 remove_effect=None,
                 max_duration=None, max_stack=None):
        
        self.trigger = trigger
        self.effect = effect
        self.condition = condition
        self.max_duration = max_duration
        self.max_stack = max_stack
        self.remove_effect = remove_effect
        
        self.is_active = False        
        self.current_duration = 0
        self.current_stack = 0
        
    def check_and_apply(self, holder, character, battle, **kwargs):
        if self.trigger and self.trigger(character, battle, **kwargs):
            if not(self.condition) or (self.condition and self.condition(character, battle, **kwargs)):
                if self.effect:
                    print(f"{character.name}'s {holder.name} has triggered")
                    time.sleep(1)
                    self.effect(character, battle, **kwargs)
                    self.is_active = True
                    self.current_stack += 1
                    
    def check_and_remove(self, holder, character, battle, **kwargs):
        if self.is_active and (self.max_duration and self.current_duration > self.max_duration):
            if self.remove_effect:
                print(f"{character.name}'s {holder.name} has deactivated")
                time.sleep(1)
                self.remove_effect(character, battle, **kwargs)
                self.is_active = False
                self.current_duration = 0


    
    
# Trigger Conditions
def trigger_on_start_of_battle(character, battle, **kwargs): # At the start of battle
    return kwargs.get("trigger") == "on_start_of_battle"

# Attack Triggers
def trigger_before_attack(character, battle, **kwargs):  # Before executing an attack
    return kwargs.get("trigger") == "before_attack"

def trigger_after_attack(character, battle, **kwargs):  # After executing an attack
    return kwargs.get("trigger") == "after_attack"

def trigger_before_receive_attack(character, battle, **kwargs): # After receiving an attack
    return kwargs.get("trigger") == "before_receive_attack"

def trigger_after_receive_attack(character, battle, **kwargs): # After receiving an attack
    return kwargs.get("trigger") == "after_receive_attack"


# Turn Triggers
def trigger_on_turn_x(x):  # At the start of turn (X)
    return lambda character, battle, **kwargs: kwargs.get("trigger") == "on_start_of_turn" and battle.turn == x

def trigger_on_start_of_turn(character, battle, **kwargs):  # At the start of turn
    return kwargs.get("trigger") == "on_start_of_turn"


def trigger_on_start_of_character_turn(character, battle, **kwargs): # At the start of your turn
    return kwargs.get("trigger") == "on_start_of_character_turn"


# Death Triggers
def trigger_on_death_by_ally(character, battle, **kwargs): # After dying by an ally's attack
    return kwargs.get("trigger") == "on_death_by_ally"


def trigger_on_death_by_enemy(character, battle, **kwargs): # After dying by an enemy's attack
    return kwargs.get("trigger") == "on_death_by_enemy"


# Stat Triggers
def trigger_on_stat_threshold(condition): # When (STAT) is (CONDITION) (THRESHOLD)
    return lambda character, battle, **kwargs: condition(character)


def trigger_if_ally_present(name): # If an ally with the name (NAME) is present
    return lambda character, battle, **kwargs: any(ally.name == name for ally in battle.get_character_allies(character))



