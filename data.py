from characters import Character
from runes import Rune
from effects import ActiveEffect, PassiveEffect, StatusEffect
import effects
import random
import time

# Active Effects
def large_slice(character, battle):
    target = battle.choose_target(battle.get_all_characters(), character)
    if target:
        print(f"{character.name} attacks {target.name}!")
        multiplier = random.uniform(1.0, 1.5)
        damage = max(character.attack + 1, int(character.attack * multiplier))
        target.receive_attack(damage, character, battle)
        time.sleep(1)
        
effect_large_slice = ActiveEffect("Large Slice", description="Attacks the target. Dealing (100% - 150%) of ATK as Damage", effect_function=large_slice)

def heal_all_allies(character, battle):
    for ally in battle.get_character_allies(character):
        heal_amount = max(1, ally.max_hp * 0.05)
        ally.receive_heal(heal_amount)
        time.sleep(1)

effect_heal_all = ActiveEffect("Heal All", description="All allies heal health equal to 5% of MAXHP", effect_function=heal_all_allies)

def swap_atk_def(character, battle):
    character.attack, character.defense = character.defense, character.attack
    print(f"{character.name} swapped ATK and DEF stats.")
    time.sleep(1)

effect_guard_switch = ActiveEffect("Guard Switch", description="Swaps the character's ATK and DEF Stats", effect_function=swap_atk_def)

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

effect_enforced_vigor = ActiveEffect(
    "Enforced Vigor", description="Attacks the target. Dealing 50% of ATK as Damage. If the target is an ally. Attacks the target. Dealing 180% of ATK as Damage and poison a random enemy for 3 turns.",
    effect_function=damage_ally_and_poison_enemy)





# Passive Effects
def thousand_divine_cuts(character, battle):
    for enemy in battle.get_character_enemies(character):
        old_defense = enemy.defense
        enemy.defense = min(enemy.defense - 1, int(enemy.defense * 0.95))
        print(f"{enemy.name} DEF reduced by 5% {old_defense} -> {enemy.defense}")
        
effect_thousand_divine_cuts = PassiveEffect("Thousand Divine Cuts", description="At the start of battle, All enemies have DEF reduced by 5%", 
                            effect_function=thousand_divine_cuts, trigger_condition=effects.trigger_on_start_of_battle)


def early_stance(character, battle):
    old_defense = character.defense
    character.defense = max(character.defense + 1, int(character.defense * 1.2))
    print(f"{character.name} enters an early stance. DEF increased by 20%. {old_defense} -> {character.defense}")

effect_early_stance = PassiveEffect("Early Stance", description="For 5 turns, Increase DEF by 20%",
                                    effect_function=early_stance, trigger_condition=effects.trigger_within_first_x_turns(5))

def engine(character, battle):
    old_speed = character.speed
    character.speed += 1
    print(f"{character.name} SPD increased by 1. {old_speed} -> {character.speed}")
    
effect_engine = PassiveEffect("Engine", description="After receiving an attack, SPD + 1",
                              effect_function=engine, trigger_condition=effects.trigger_on_receive_attack)


def double_up(character, battle):
    old_attack = character.attack
    character.attack = max(character.attack + 1, int(character.attack * 1.01))
    print(f"{character.name} ATK increased by 1%. {old_attack} -> {character.attack}")
    
effect_double_up = PassiveEffect("Double Up", description="After executing an attack, Increase ATK by 1%",
                                 effect_function=double_up, trigger_condition=effects.trigger_on_attack)


def late_bloomer(character, battle):
    character.hp = character.max_hp
    print(f"{character.name} fully recovers HP.")
    
effect_late_bloomer = PassiveEffect("Late Bloomer", description="On Turn 2, Fully recover HP",
                                    effect_function=late_bloomer, trigger_condition=effects.trigger_on_turn_x(2))


def last_stance(character, battle):
    old_attack = character.attack
    character.attack = max(character.attack + 1, int(character.attack * 1.5))
    print(f"{character.name} ATK increased by 50%. {old_attack} -> {character.attack}")
    
effect_last_stance = PassiveEffect("Last Stance", description="When HP is below 50%. Increase ATK by 50%", effect_function=last_stance,
                                   trigger_condition=effects.trigger_on_stat_threshold("hp", lambda hp, character: hp < character.max_hp / 2))


def wolf_hunger(character, battle):
    for ally in battle.get_character_allies(character):
        old_attack = ally.attack
        ally.attack = max(ally.attack + 1, int(ally.attack * 1.5))
        print(f"{ally.name} ATK increased by 50%. {old_attack} -> {ally.attack}")
        
effect_wolf_hunger = PassiveEffect("Wolf Hunger", description="When killed by an enemy. Increase allies ATK by 50%",
                                   effect_function=wolf_hunger, trigger_condition=effects.trigger_on_death_by_enemy)
        
   
   
        
# Status Effects
def poison(character, battle):
    damage = character.max_hp * 0.06
    print(f"{character.name} is poisoned")
    character.take_damage(damage, battle)
    
effect_status_poison = StatusEffect("Poison", description="Takes 6% of Max HP as damage at the start of turn", duration=3, ongoing_effect=poison, trigger_condition=effects.trigger_on_start_of_turn)




# Runes
power_rune = Rune(
    name="Power Rune",
    active_effects=[effect_large_slice, effect_enforced_vigor],
    passive_effects=[effect_thousand_divine_cuts, effect_early_stance, effect_double_up, effect_engine, effect_late_bloomer, effect_last_stance, effect_wolf_hunger]
)

crystalised_ice_rune = Rune(
    name="Crystalised Ice Rune",
    active_effects=[effect_guard_switch]
)

glowing_grass_rune = Rune(
    name="Glowing Grass Rune",
    active_effects=[effect_heal_all]
)



# Characters
chr_azelgram = Character(
    name="Azelgram",
    max_hp=100,
    attack=10,
    defense=10,
    speed=10,
    runes=[]
    description=
    """
        Azelgram, The Devourer of Spirits, The Demon of Belief, The Fireborn Horror.
        A demon of pure evil. A being created from supernatural.
        Which is led by humanity's sole belief that demon's truly exist in this world.
        Azelgram is a demon that feeds on the souls of the living. 
        He gained their memories, their knowledge, their power, and their essence.
        He learnt everything about the world. Including the supernatural.
        He is a being of pure darkness and malice.
        After enough souls, he grew wings made of an eldritch horror.      
    """
)