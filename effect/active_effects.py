from character.characters import Damage
from effect.effect_base import ActiveEffect
import effect.status_effects as status_effects
import random
import time

# Rune Force
RUNE_FORCE = ActiveEffect(
    "Rune Force",
    description="Attacks the target. Dealing 120% of ATK as Damage",
    effect_function=lambda character, battle: _rune_force(character, battle)
)
def _rune_force(character, battle):
    target = battle.choose_target(battle.get_all_characters(), character)
    if target:
        print(f"{character.name} attacks {target.name}!")
        multiplier = 1.2
        damage_amount = max(character.attack.total + 1, round(character.attack.total * multiplier))
        damage = Damage()
        damage.build(damage_amount, character, target)
        target.receive_attack(damage, character, battle)
        time.sleep(1)
        

# Large Slice
LARGE_SLICE = ActiveEffect(
    "Large Slice",
    description="Attacks the target. Dealing (100% - 150%) of ATK as Damage",
    effect_function=lambda character, battle: _large_slice(character, battle)
)
def _large_slice(character, battle):
    target = battle.choose_target(battle.get_all_characters(), character)
    if target:
        print(f"{character.name} attacks {target.name}!")
        multiplier = random.uniform(1.0, 1.5)
        damage = Damage()
        damage.build(max(character.attack.total + 1,
                     int(character.attack.total * multiplier)), character, target)
        target.receive_attack(damage, character, battle)
        time.sleep(1)



# Guard Switch
GUARD_SWITCH = ActiveEffect(
    "Guard Switch",
    description="Swaps the character's ATK and DEF Stats",
    effect_function=lambda character, battle: _swap_atk_def(character, battle))

def _swap_atk_def(character, battle):
    character.attack, character.defense = character.defense, character.attack
    character.attack.name, character.defense.name = character.defense.name, character.attack.name
    print(f"{character.name} swapped ATK and DEF stats.")
    time.sleep(1)



# Enforced Vigor
ENFORCED_VIGOR = ActiveEffect(
    "Enforced Vigor",
    description="Attacks the target. Dealing 50% of ATK as Damage. If the target is an ally. Attacks the target. Dealing 180% of ATK as Damage and poison a random enemy for 3 turns.",
    effect_function=lambda character, battle: _damage_ally_and_poison_enemy(character, battle))

def _damage_ally_and_poison_enemy(character, battle):
    target = battle.choose_target(battle.get_all_characters(), character)
    if (target in battle.get_character_allies(character)) and (target != character):
        # Deal Damage
        print(f"{character.name} attacks {target.name}!")
        damage = Damage()
        damage.build(max(character.attack.total + 1,
                     int(character.attack.total * 1.8)), character, target)
        target.receive_attack(damage, character, battle)

        # Poison
        random_enemy = random.choice(battle.get_character_enemies(character))
        poison = status_effects.POISON
        poison.max_duration = 3
        random_enemy.add_status_effect(poison)

    else:
        # Deal Damage
        print(f"{character.name} attacks {target.name}!")
        damage = Damage()
        damage.build(int(character.attack.total * 0.5), character, target)
        target.receive_attack(damage, character, battle)


POLISH = ActiveEffect(
    "Polish",
    description="Increases all allies DEF by 5% for 3 turns.",
    effect_function=lambda character, battle: _polish(character, battle)
)

# Polish
def _polish(character, battle):
    for target in battle.get_character_allies(character):
        old_defense = target.defense.total
        target.defense.add_modifier(1.05, is_multiplicative=True)
        print(
            f"{target.name} DEF increased by 5% {old_defense} -> {target.defense.total}")




# Gale Lightning
GALE_LIGHTNING = ActiveEffect(
    "Gale Lightning", description="Attacks the target. Dealing 100% of ATK as Damage and Increases own SPD by 10% for 2 turns.",
    effect_function=lambda character, battle: _gale_lightning(character, battle)
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
def evasive_agility(character, battle):
    old_evasion = character.evasion.total
    character.evasion.add_modifier(1.15, is_multiplicative=True)
    print(f"{character.name} EV increased by 15% {old_evasion} -> {character.evasion.total}")


EVASIVE_AGILITY = ActiveEffect(
    "Evasive Agility", description="+15% Evasion for 3 turns.",
    effect_function=evasive_agility
)

# Unstable Strength
def unstable_strength(character, battle):
    target = battle.choose_target(battle.get_all_characters(), character)
    if target:
        print(f"{character.name} attacks {target.name}!")
        multiplier = random.uniform(0.9, 1.5)
        damage = Damage()
        damage.build(max(character.attack.total + 1,
                     int(character.attack.total * multiplier)), character, target)
        damage.ignore_defense -= 0.2
        target.receive_attack(damage, character, battle)
        time.sleep(1)


UNSTABLE_STRENGTH = ActiveEffect(
    "Unstable Strength", description="Deals (90 - 150)% ATK as Damage to the target. This attack ignores 20% of the target's DEF.",
    effect_function=unstable_strength)


# Dark Pit
def dark_pit(character, battle):
    dead_characters = len(
        [chr for chr in battle.get_all_characters() if not (chr.is_alive())])
    for enemy in battle.get_character_enemies(character):
        print(f"{character.name} attacks {enemy.name}!")
        damage = Damage()
        multiplier = 0.3 + (0.5 * dead_characters)
        damage.build(int(character.attack.total *
                     multiplier), character, enemy)
        enemy.receive_attack(damage, character, battle)


DARK_PIT = ActiveEffect(
    "Dark Pit", description="Deals 30% of ATK as Damage to all enemies. Increase multiplier by 50% for every dead character in battle.",
    effect_function=dark_pit)
