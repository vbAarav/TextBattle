from character.characters import Damage
from effect.effects import PassiveEffect
import effect.effects as effects


# Thousand Divine Cuts
def thousand_divine_cuts(character, battle):
    for enemy in battle.get_character_enemies(character):
        old_defense = enemy.defense.total
        enemy.defense.add_modifier(0.95, is_multiplicative=True)
        print(f"{enemy.name} DEF reduced by 5% {old_defense} -> {enemy.defense.total}")


THOUSAND_DIVINE_CUTS = PassiveEffect("Thousand Divine Cuts", description="At the start of battle, All enemies have DEF reduced by 5%",
                                     apply_function=thousand_divine_cuts, apply_trigger=effects.trigger_on_start_of_battle)

# Early Stance
def early_stance(character, battle):
    old_defense = character.defense.total
    character.defense.add_modifier(1.2, is_multiplicative=True)
    print(f"{character.name} DEF increased by 20%. {old_defense} -> {character.defense.total}")
    
def early_stance_remove(character, battle):
    old_defense = character.defense.total
    character.defense.remove_modifier(1.2, is_multiplicative=True)
    print(f"{character.name} DEF decreased by 20%. {old_defense} -> {character.defense.total}")

EARLY_STANCE = PassiveEffect("Early Stance", description="At the start of battle, Increase DEF by 20% for 5 turns",
                             apply_function=early_stance, apply_trigger=effects.trigger_on_start_of_battle,
                             remove_function=early_stance_remove, remove_trigger=effects.trigger_on_turn_x(6))

# Engine
def engine(character, battle):
    old_speed = character.speed.total
    character.speed.add_modifier(1)
    print(f"{character.name} SPD increased by 1. {old_speed} -> {character.speed.total}")


ENGINE = PassiveEffect("Engine", description="After receiving an attack, SPD + 1",
                              apply_function=engine, apply_trigger=effects.trigger_after_receive_attack)

# Double Up
def double_up(character, battle):
    old_attack = character.attack.total
    character.attack.add_modifier(1.03, is_multiplicative=True)
    print(f"{character.name} ATK increased by 3%. {old_attack} -> {character.attack.total}")

DOUBLE_UP = PassiveEffect("Double Up", description="After executing an attack, Increase ATK by 3%", apply_function=double_up, apply_trigger=effects.trigger_after_attack)

# Late Bloomer
def late_bloomer(character, battle):
    old_hp = character.max_hp.total
    character.max_hp.change_resource_by_perc(0.05)
    print(f"{character.name} HP increased by 5%. {old_hp} -> {character.max_hp.total}")

LATE_BLOOMER = PassiveEffect("Late Bloomer", description="At the start of turn 2, Increase HP by 5%", apply_function=late_bloomer, apply_trigger=effects.trigger_on_turn_x(2), max_stack=1)

# Last Stance
def last_stance(character, battle):
    old_attack = character.attack.total
    character.attack.add_modifier(1.5, is_multiplicative=True)
    print(f"{character.name} ATK increased by 50%. {old_attack} -> {character.attack.total}")


LAST_STANCE = PassiveEffect("Last Stance", description="When HP is below 50%. Increase ATK by 50%",
                            apply_function=last_stance, apply_trigger=effects.trigger_on_stat_threshold(lambda character: character.max_hp.get_percentage() < 0.5), max_stack=1)

# Wolf Hunger
def wolf_hunger(character, battle):
    for ally in battle.get_character_allies(character):
        old_attack = ally.attack.total
        ally.attack.add_modifier(1.5, is_multiplicative=True)
        print(f"{ally.name} ATK increased by 50%. {old_attack} -> {ally.attack.total}")


WOLF_HUNGER = PassiveEffect("Wolf Hunger", description="When killed by an enemy. Increase allies ATK by 50%", apply_function=wolf_hunger, apply_trigger=effects.trigger_on_death_by_enemy)

# Burning Adrenaline
def burning_adrenaline(character, battle):
    old_crit_chance = character.crit_chance.total
    character.crit_chance.add_modifier(0.03)
    print(f"{character.name} CRIT CHANCE increased by 3% {old_crit_chance * 100}% -> {character.crit_chance.total * 100}%")


BURNING_ADRENALINE = PassiveEffect("Burning Adrenaline", description="At the start of battle, Increase Crit Chance by 3%",
                                          apply_function=burning_adrenaline, apply_trigger=effects.trigger_on_start_of_battle)
# Harden
def harden(character, battle):
    old_res = character.resistance.total
    character.resistance.add_modifier(1.03, is_multiplicative=True)
    print(f"{character.name} RES increased by 3% {old_res} -> {character.resistance.total}")


HARDEN = PassiveEffect("Harden", description="At the start of battle, Increase Resistance by 3%",
                              apply_function=harden, apply_trigger=effects.trigger_on_start_of_battle)

# Flowing Ring
def flowing_ring(character, battle):
    old_hp = character.max_hp.total
    character.max_hp.add_modifier(1.03, is_multiplicative=True)
    print(f"{character.name} MAXHP increased by 3% {old_hp} -> {character.max_hp.total}")


FLOWING_RING = PassiveEffect("Flowing Ring", description="At the start of battle, Increase MAXHP by 3%",
                                    apply_function=flowing_ring, apply_trigger=effects.trigger_on_start_of_battle)

# Quick Boots
def quick_boots(character, battle):
    old_spd = character.speed.total
    character.speed.add_modifier(1.03, is_multiplicative=True)
    print(f"{character.name} SPD increased by 3% {old_spd} -> {character.speed.total}")


QUICK_BOOTS = PassiveEffect("Quick Boots", description="At the start of battle, Increase SPD by 3%",
                                   apply_function=quick_boots, apply_trigger=effects.trigger_on_start_of_battle)

# Early Feast
def early_feast(character, battle):
    old_atk = character.attack.total
    old_crit_chance = character.crit_chance.total
    character.attack.add_modifier(1.5, is_multiplicative=True)
    character.crit_chance.add_modifier(0.5)
    print(f"{character.name} ATK increased by 50% {old_atk} -> {character.attack.total}")
    print(f"{character.name} CRIT CHANCE increased by 50% {old_crit_chance * 100}% -> {character.crit_chance.total * 100}%")
    
def early_feast_remove(character, battle):
    old_atk = character.attack.total
    old_crit_chance = character.crit_chance.total
    character.attack.remove_modifier(1.5, is_multiplicative=True)
    character.crit_chance.remove_modifier(0.5)
    print(f"{character.name} ATK decreased by 50% {old_atk} -> {character.attack.total}")
    print(f"{character.name} CRIT CHANCE decreased by 50% {old_crit_chance * 100}% -> {character.crit_chance.total * 100}%")


EARLY_FEAST = PassiveEffect("Early Feast", description="At the start of battle, Increase ATK and Crit Chance by 50% for 2 turns",
                                   apply_function=early_feast, apply_trigger=effects.trigger_on_start_of_battle,
                                   remove_function=early_feast_remove, remove_trigger=effects.trigger_on_turn_x(3))

# Demon Hunger
def demon_hunger(character, battle):
    old_attack = character.attack.total
    character.attack.add_modifier(1.2, is_multiplicative=True)
    print(f"{character.name} ATK increased by 20%. {old_attack} -> {character.attack.total}")


DEMON_HUNGER = PassiveEffect("Demon Hunger", description="Before attacking, if the target is a 'Demon', Increase ATK by 10% and inflict burn on the target.",
                                   apply_function=demon_hunger, apply_trigger=effects.trigger_before_attack, 
                                   apply_condition=lambda character, battle, **kwargs: kwargs.get("target").race and kwargs.get("target").race == "Demon")

# Death Will Arrive
def death_will_arrive(character, battle):
    for enemy in battle.get_character_enemies(character):
        if not (enemy.is_alive()):
            old_attack = character.attack.total
            character.attack.add_modifier(1.2, is_multiplicative=True)
            print(
                f"{character.name} ATK increased by 20%. {old_attack} -> {character.attack.total}")


DEATH_WILL_ARRIVE = PassiveEffect("Death Will Arrive", description="After attacking, if the target is dead, increase ATK by 20% of the target's ATK",
                                         apply_function=death_will_arrive, apply_trigger=effects.trigger_after_attack, 
                                         apply_condition=lambda character, battle, **kwargs: kwargs.get("target").is_alive() == False)
