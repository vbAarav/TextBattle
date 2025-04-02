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
    def __init__(self, name, description="", apply_function=None, apply_trigger=None, apply_condition=None, max_stack=None, remove_function=None, remove_trigger=None):
        super().__init__(name, description)
        self.apply_function = apply_function  # Function to apply the passive effect
        self.apply_trigger = apply_trigger
        self.apply_condition = apply_condition  # Condition to apply the effect
        self.remove_function = remove_function  # Function to remove the effect
        self.remove_trigger = remove_trigger  # Condition to remove the effect
        self.max_stack = max_stack  # Maximum number of stacks for the effect
        
        self.is_active = False
        self.current_stack = 0  # Current number of stacks for the effect
        
        
    def check(self, character, battle, **kwargs):
        if not(self.max_stack) or (self.current_stack < self.max_stack):
            self.check_and_apply(character, battle, **kwargs)
        if self.is_active:
            self.check_and_remove(character, battle, **kwargs)

    def check_and_apply(self, character, battle, **kwargs):
        """Checks if the condition is met and applies the effect if so."""
        if self.apply_trigger and self.apply_trigger(character, battle, **kwargs):
            if not(self.apply_condition) or self.apply_condition(character, battle, **kwargs):
                print(f"{character.name}'s {self.name} is triggered.")
                time.sleep(1)
                self.apply(character, battle)
                self.is_active = True
                self.current_stack += 1
            
    def check_and_remove(self, character, battle, **kwargs):
        """Checks if the remove condition is met and removes the effect if so."""
        if self.remove_trigger and self.remove_trigger(character, battle, **kwargs):
            print(f"{character.name}'s {self.name} no longer has any effect.")
            time.sleep(1)
            self.remove(character, battle)
            self.is_active = False
            self.current_stack -= 1

    def apply(self, character, battle):
        # Passive effects may be triggered on certain events automatically
        if self.apply_function:
            self.apply_function(character, battle)
            
    def remove(self, character, battle):
        if self.remove_function:
            self.remove_function(character, battle)

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
    return lambda character, battle, **kwargs: battle.turn == x

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
