from character.characters import Damage
from effect.effect_base import ActiveEffect
import effect.status_effects as status_effects
import random
import time
import copy

# Rune Force
RUNE_FORCE = ActiveEffect(
    "Rune Force",
    description="Attacks the target. Dealing damage equal to 120% of ATK. This damage increase by 5% for each rune on the equipped sigil.",
    effect_function=lambda character, battle, **kwargs: _rune_force(character, battle, **kwargs)
)
def _rune_force(character, battle, **kwargs):
    target = battle.choose_target(battle.get_all_characters(), character)
    if target:
        print(f"{character.name} attacks {target.name}!")

        # Calculate Multiplier
        multiplier = 1.2
        if 'sigil' in kwargs and kwargs['sigil']:
            multiplier += 0.05 * len(kwargs['sigil'].rune_composition.values())
          
        # Calculate Damage
        damage_amount = max(character.attack.total + 1, round(character.attack.total * multiplier))
        damage = Damage()
        damage.build(damage_amount, character, target)
        target.receive_attack(damage, character, battle)
        time.sleep(1)
        

# Large Slice
LARGE_SLICE = ActiveEffect(
    "Large Slice",
    description="Attacks the target. Dealing damage equal to (100% - 150%) of ATK",
    effect_function=lambda character, battle, **kwargs: _large_slice(character, battle)
)
def _large_slice(character, battle):
    target = battle.choose_target(battle.get_all_characters(), character)
    if target:
        print(f"{character.name} attacks {target.name}!")
        multiplier = random.uniform(1.0, 1.5)
        damage = Damage()
        damage.build(max(character.attack.total + 1, int(character.attack.total * multiplier)), character, target)
        target.receive_attack(damage, character, battle)
        time.sleep(1)



# Guard Switch
GUARD_SWITCH = ActiveEffect(
    "Guard Switch",
    description="Swaps the character's ATK and DEF Stats",
    effect_function=lambda character, battle, **kwargs: _swap_atk_def(character, battle))

def _swap_atk_def(character, battle):
    character.attack, character.defense = character.defense, character.attack
    character.attack.name, character.defense.name = character.defense.name, character.attack.name
    print(f"{character.name} swapped ATK and DEF stats.")
    time.sleep(1)



# Enforced Vigor
ENFORCED_VIGOR = ActiveEffect(
    "Enforced Vigor",
    description="Attacks the target. Dealing damage equal to 50% of ATK. If the target is an ally, This damage increases by 180% and poison a random enemy for 3 turns.",
    effect_function=lambda character, battle, **kwargs: _damage_ally_and_poison_enemy(character, battle))

def _damage_ally_and_poison_enemy(character, battle):
    target = battle.choose_target(battle.get_all_characters(), character)
    if (target in battle.get_character_allies(character)) and (target != character):
        # Deal Damage
        print(f"{character.name} attacks {target.name}!")
        damage_amount = max(character.attack.total + 1, round(character.attack.total * (0.5 + 1.8)))
        damage = Damage()
        damage.build(damage_amount, character, target)
        target.receive_attack(damage, character, battle)
        time.sleep(1)

        # Poison
        random_enemy = random.choice(battle.get_character_enemies(character))
        poison = copy.deepcopy(status_effects.POISON)
        poison.max_duration = 3
        random_enemy.add_status_effect(poison, battle)

    else:
        # Deal Damage
        print(f"{character.name} attacks {target.name}!")
        damage = Damage()
        damage.build(int(character.attack.total * 0.5), character, target)
        target.receive_attack(damage, character, battle)

# Polish
POLISH = ActiveEffect(
    "Polish",
    description="Increases all allies DEF by 5% for 3 turns.",
    effect_function=lambda character, battle, **kwargs: _polish(character, battle)
)
def _polish(character, battle):
    for target in battle.get_character_allies(character):
        old_defense = target.defense.total
        target.defense.add_modifier(1.05, is_multiplicative=True)
        print(
            f"{target.name} DEF increased by 5% {old_defense} -> {target.defense.total}")


# Gale Lightning
GALE_LIGHTNING = ActiveEffect(
    "Gale Lightning",
    description="Attacks the target. Dealing damage equal to 100% of ATK. Increases SPD by 10% for 2 turns.",
    effect_function=lambda character, battle, **kwargs: _gale_lightning(character, battle)
)

def _gale_lightning(character, battle):
    # Deal Damage
    target = battle.choose_target(battle.get_all_characters(), character)
    print(f"{character.name} attacks {target.name}!")
    damage = Damage()
    damage.build(max(character.attack.total + 1,
                 int(character.attack.total * 1.8)), character, target)
    target.receive_attack(damage, character, battle)

    # Speed Increase
    old_speed = character.speed.total
    character.speed.add_modifier(1.1, is_multiplicative=True)
    print(f"{character.name} SPD increased by 10% {old_speed} -> {character.speed.total}")


# Evasive Agility
EVASIVE_AGILITY = ActiveEffect(
    "Evasive Agility",
    description="Increases Evasion by 15% for 3 turns.",
    effect_function=lambda character, battle, **kwargs: _evasive_agility(character, battle)
)
def _evasive_agility(character, battle):
    old_evasion = character.evasion.total
    character.evasion.add_modifier(1.15, is_multiplicative=True)
    print(f"{character.name} EV increased by 15% {old_evasion} -> {character.evasion.total}")


# Unstable Strength
UNSTABLE_STRENGTH = ActiveEffect(
    "Unstable Strength",
    description="Attacks the target. Dealing damage equal to (90% - 150%) of ATK. This attack ignores 20% of the target's DEF.",
    effect_function=lambda character, battle, **kwargs: _unstable_strength(character, battle))

def _unstable_strength(character, battle):
    target = battle.choose_target(battle.get_all_characters(), character)
    if target:
        print(f"{character.name} attacks {target.name}!")
        multiplier = random.uniform(0.9, 1.5)
        damage = Damage()
        damage.build(max(character.attack.total + 1, int(character.attack.total * multiplier)), character, target)
        damage.ignore_defense -= 0.2
        target.receive_attack(damage, character, battle)
        time.sleep(1)


# Dark Pit
DARK_PIT = ActiveEffect(
    "Dark Pit",
    description="Attacks all enemies. Dealing damage equal to 130% of ATK. This damage increases by 50% for every dead character in battle.",
    effect_function=lambda character, battle, **kwargs: _dark_pit(character, battle))

def _dark_pit(character, battle):
    dead_characters = len([chr for chr in battle.get_all_characters() if not (chr.is_alive())])
    for enemy in battle.get_character_enemies(character):
        print(f"{character.name} attacks {enemy.name}!")
        damage = Damage()
        multiplier = 1.3 + (0.5 * dead_characters)
        damage.build(int(character.attack.total *
                     multiplier), character, enemy)
        enemy.receive_attack(damage, character, battle)



