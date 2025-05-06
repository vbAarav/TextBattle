from effect.effect_base import ComplexEffect, PassiveEffect
import effect.effect_base as effect_base
import effect.status_effects as status_effects
import copy


# Special Intimidate
SPECIAL_INTIMIDATE = PassiveEffect(
    "Special Intimidate",
     description="At the start of battle, Decrease all enemies DEF by 10% and inflict Stun for 1 turn",
     effects=
     [
        ComplexEffect(effect_base.trigger_on_start_of_battle, lambda character, battle, **kwargs: special_intimidate(character, battle, **kwargs)),
        ComplexEffect(effect_base.trigger_on_start_of_battle, lambda character, battle, **kwargs: special_intimidate_stun(character, battle, **kwargs))
     ]
)
def special_intimidate(character, battle, **kwargs):
    for enemy in battle.get_character_enemies(character):
        old_defense = enemy.defense.total
        enemy.defense.add_modifier(0.90, is_multiplicative=True)
        print(f"{enemy.name} DEF reduced by 10% {old_defense} -> {enemy.defense.total}")

def special_intimidate_stun(character, battle, **kwargs):
    for enemy in battle.get_character_enemies(character):
        stun = copy.deepcopy(status_effects.STUN)
        stun.max_duration = 2
        enemy.add_status_effect(stun, battle)
        



# Early Stance
EARLY_STANCE = PassiveEffect(
    "Early Stance",
     description="At the start of battle, Increase DEF by 20% for 5 turns",
     effects=
     [
        ComplexEffect(effect_base.trigger_on_start_of_battle, lambda character, battle, **kwargs: early_stance(character, battle, **kwargs), max_duration=5, remove_effect=lambda character, battle, **kwargs: early_stance_remove(character, battle, **kwargs))
     ]
)

def early_stance(character, battle, **kwargs):
    old_defense = character.defense.total
    character.defense.add_modifier(1.2, is_multiplicative=True)
    print(f"{character.name} DEF increased by 20%. {old_defense} -> {character.defense.total}")
    
def early_stance_remove(character, battle, **kwargs):
    old_defense = character.defense.total
    character.defense.remove_modifier(1.2, is_multiplicative=True)
    print(f"{character.name} DEF decreased by 20%. {old_defense} -> {character.defense.total}")
    

# Engine
ENGINE = PassiveEffect(
    "Engine",
     description="After receiving an attack, SPD + 1",
     effects=[ComplexEffect(effect_base.trigger_after_receive_attack, lambda character, battle, **kwargs : engine(character, battle, **kwargs))]
)

def engine(character, battle, **kwargs):
    old_speed = character.speed.total
    character.speed.add_modifier(1)
    print(f"{character.name} SPD increased by 1. {old_speed} -> {character.speed.total}")


# Double Up
DOUBLE_UP = PassiveEffect(
    "Double Up",
     description="After executing an attack, Increase ATK by 3%",
     effects=[ComplexEffect(effect_base.trigger_after_attack, lambda character, battle, **kwargs: double_up(character, battle, **kwargs))]
)
def double_up(character, battle, **kwargs):
    old_attack = character.attack.total
    character.attack.add_modifier(1.03, is_multiplicative=True)
    print(f"{character.name} ATK increased by 3%. {old_attack} -> {character.attack.total}")

# Late Bloomer
LATE_BLOOMER = PassiveEffect(
    "Late Bloomer",
     description="At the start of turn 2, Increase HP by 5%",
     effects=
     [
        ComplexEffect(effect_base.trigger_on_turn_x(2), lambda character, battle, **kwargs: late_bloomer(character, battle, **kwargs))
     ]
)
def late_bloomer(character, battle, **kwargs):
    old_hp = character.max_hp.total
    character.max_hp.change_resource_by_perc(0.05)
    print(f"{character.name} HP increased by 5%. {old_hp} -> {character.max_hp.total}")



# Last Stance
LAST_STANCE = PassiveEffect(
    "Last Stance",
    description="The first time HP is below 50%. Increase ATK by 50%",
    effects=[
        ComplexEffect(effect_base.trigger_on_stat_threshold(lambda character: character.max_hp.get_percentage() < 0.5), lambda character, battle, **kwargs: last_stance(character, battle, **kwargs), max_stack=1)
    ]
)
def last_stance(character, battle, **kwargs):
    old_attack = character.attack.total
    character.attack.add_modifier(1.5, is_multiplicative=True)
    print(f"{character.name} ATK increased by 50%. {old_attack} -> {character.attack.total}")


# Wolf Hunger
WOLF_HUNGER = PassiveEffect(
    "Wolf Hunger",
     description="When killed by an enemy. Increase allies ATK by 50%",
     effects=[
        ComplexEffect(effect_base.trigger_on_death_by_enemy, lambda character, battle, **kwargs: wolf_hunger(character, battle, **kwargs))
     ]
)
def wolf_hunger(character, battle, **kwargs):
    for ally in battle.get_character_allies(character):
        old_attack = ally.attack.total
        ally.attack.add_modifier(1.5, is_multiplicative=True)
        print(f"{ally.name} ATK increased by 50%. {old_attack} -> {ally.attack.total}")



# Burning Adrenaline
BURNING_ADRENALINE = PassiveEffect(
    "Burning Adrenaline",
     description="At the start of battle, Increase Crit Chance by 3%",
     effects=[
         ComplexEffect(effect_base.trigger_on_start_of_battle, lambda character, battle, **kwargs: burning_adrenaline(character, battle, **kwargs))
    ]
)
def burning_adrenaline(character, battle, **kwargs):
    old_crit_chance = character.crit_chance.total
    character.crit_chance.add_modifier(0.03)
    print(f"{character.name} CRIT CHANCE increased by 3% {old_crit_chance * 100}% -> {character.crit_chance.total * 100}%")


# Harden
HARDEN = PassiveEffect(
    "Harden",
    description="At the start of battle, Increase Resistance by 3%",
    effects=[
        ComplexEffect(effect_base.trigger_on_start_of_battle, lambda character, battle, **kwargs: harden(character, battle, **kwargs))
    ]
)
def harden(character, battle, **kwargs):
    old_res = character.resistance.total
    character.resistance.add_modifier(1.03, is_multiplicative=True)
    print(f"{character.name} RES increased by 3% {old_res} -> {character.resistance.total}")




# Flowing Ring
FLOWING_RING = PassiveEffect(
    "Flowing Ring",
     description="At the start of battle, Increase MAXHP by 3%",
     effects=[
         ComplexEffect(effect_base.trigger_on_start_of_battle, lambda character, battle, **kwargs: flowing_ring(character, battle, **kwargs))
    ]
)
def flowing_ring(character, battle, **kwargs):
    old_hp = character.max_hp.total
    character.max_hp.add_modifier(1.03, is_multiplicative=True)
    print(f"{character.name} MAXHP increased by 3% {old_hp} -> {character.max_hp.total}")



# Quick Boots
QUICK_BOOTS = PassiveEffect(
    "Quick Boots",
    description="At the start of battle, Increase SPD by 3%",
    effects=
    [
        ComplexEffect(effect_base.trigger_on_start_of_battle, lambda character, battle, **kwargs: quick_boots(character, battle, **kwargs))
    ]
)
def quick_boots(character, battle, **kwargs):
    old_spd = character.speed.total
    character.speed.add_modifier(1.03, is_multiplicative=True)
    print(f"{character.name} SPD increased by 3% {old_spd} -> {character.speed.total}")


# Early Feast
EARLY_FEAST = PassiveEffect(
    "Early Feast",
     description="At the start of battle, Increase ATK and Crit Chance by 50% for 2 turns",
     effects=[
        ComplexEffect(effect_base.trigger_on_start_of_battle, lambda character, battle, **kwargs: early_feast(character, battle, **kwargs), remove_effect=lambda character, battle, **kwargs: early_feast_remove(character, battle, **kwargs), max_duration=2)
    ]
)

def early_feast(character, battle, **kwargs):
    old_atk = character.attack.total
    old_crit_chance = character.crit_chance.total
    character.attack.add_modifier(1.5, is_multiplicative=True)
    character.crit_chance.add_modifier(0.5)
    print(f"{character.name} ATK increased by 50% {old_atk} -> {character.attack.total}")
    print(f"{character.name} CRIT CHANCE increased by 50% {old_crit_chance * 100}% -> {character.crit_chance.total * 100}%")
    
def early_feast_remove(character, battle, **kwargs):
    old_atk = character.attack.total
    old_crit_chance = character.crit_chance.total
    character.attack.remove_modifier(1.5, is_multiplicative=True)
    character.crit_chance.remove_modifier(0.5)
    print(f"{character.name} ATK decreased by 50% {old_atk} -> {character.attack.total}")
    print(f"{character.name} CRIT CHANCE decreased by 50% {old_crit_chance * 100}% -> {character.crit_chance.total * 100}%")


# Demon Hunger
DEMON_HUNGER = PassiveEffect(
    "Demon Hunger",
     description="Before executing an attack, if the target is a 'Demon', Increase ATK by 10% and inflict burn on the target.",
     effects=
     [
        ComplexEffect(effect_base.trigger_before_attack, lambda character, battle, **kwargs: demon_hunger, condition=lambda character, battle, **kwargs: kwargs.get("target").race and kwargs.get("target").race == "Demon")
     ]
)
def demon_hunger(character, battle, **kwargs):
    old_attack = character.attack.total
    character.attack.add_modifier(1.2, is_multiplicative=True)
    print(f"{character.name} ATK increased by 20%. {old_attack} -> {character.attack.total}")
                            

# Death Will Arrive
DEATH_WILL_ARRIVE = PassiveEffect(
    "Death Will Arrive",
     description="After executing an attack, if the target is dead, increase ATK by 20% of the target's ATK",
     effects=[
         ComplexEffect(effect_base.trigger_after_attack, lambda character, battle, **kwargs: death_will_arrive(character, battle, **kwargs), condition=lambda character, battle, **kwargs: kwargs.get("target").is_alive() == False)
    ]
)

def death_will_arrive(character, battle, **kwargs):
    for enemy in battle.get_character_enemies(character):
        if not (enemy.is_alive()):
            old_attack = character.attack.total
            character.attack.add_modifier(1.2, is_multiplicative=True)
            print(f"{character.name} ATK increased by 20%. {old_attack} -> {character.attack.total}")




# Glowing Aura
GLOWING_AURA = PassiveEffect(
    "Glowing Aura",
    description="At the start of battle, Increase Evasion by 3%",
    effects=[
        ComplexEffect(effect_base.trigger_on_start_of_battle, lambda character, battle, **kwargs: glowing_aura(character, battle, **kwargs))
    ]
)
def glowing_aura(character, battle, **kwargs):
    old_evasion = character.evasion.total
    character.evasion.add_modifier(1.03, is_multiplicative=True)
    print(f"{character.name} EV increased by 3% {old_evasion} -> {character.evasion.total}")
    

# Embrace the Darkness
EMBRACE_THE_DARKNESS = PassiveEffect(
    "Embrace the Darkness",
    description="At the start of battle, Increase SPD by 5%. The first time HP is below 20%, Increase SPD by 20%.",
    effects=[
        ComplexEffect(effect_base.trigger_on_start_of_battle, lambda character, battle, **kwargs: embrace_the_darkness_one(character, battle, **kwargs)), 
        ComplexEffect(effect_base.trigger_on_stat_threshold(lambda character: character.max_hp.get_percentage() < 0.2), lambda character, battle, **kwargs: embrace_the_darkness_two(character, battle, **kwargs), max_stack=1)
    ]
)
def embrace_the_darkness_one(character, battle, **kwargs):
    old_spd = character.speed.total
    character.speed.add_modifier(1.05, is_multiplicative=True)
    print(f"{character.name} SPD increased by 5% {old_spd} -> {character.speed.total}")
    
def embrace_the_darkness_two(character, battle, **kwargs):
    old_spd = character.speed.total
    character.speed.add_modifier(1.2, is_multiplicative=True)
    print(f"{character.name} SPD increased by 20% {old_spd} -> {character.speed.total}")


    