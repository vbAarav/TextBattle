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
                                            effect_function=thousand_divine_cuts, trigger_condition=effects.trigger_on_start_of_battle)

# Early Stance
def early_stance(character, battle):
    old_defense = character.defense.total
    character.defense.add_modifier(1.2, is_multiplicative=True)
    print(f"{character.name} enters an early stance. DEF increased by 20%. {old_defense} -> {character.defense.total}")


EARLY_STANCE = PassiveEffect("Early Stance", description="For 5 turns, Increase DEF by 20%",
                                    effect_function=early_stance, trigger_condition=effects.trigger_within_first_x_turns(5))

# Engine
def engine(character, battle):
    old_speed = character.speed.total
    character.speed.add_modifier(1)
    print(f"{character.name} SPD increased by 1. {old_speed} -> {character.speed.total}")


ENGINE = PassiveEffect("Engine", description="After receiving an attack, SPD + 1",
                              effect_function=engine, trigger_condition=effects.trigger_on_receive_attack)

# Double Up
def double_up(character, battle):
    old_attack = character.attack.total
    character.attack.add_modifier(1.03, is_multiplicative=True)
    print(f"{character.name} ATK increased by 3%. {old_attack} -> {character.attack.total}")


DOUBLE_UP = PassiveEffect("Double Up", description="After executing an attack, Increase ATK by 3%",
                                 effect_function=double_up, trigger_condition=effects.trigger_on_attack)

# Late Bloomer
def late_bloomer(character, battle):
    character.max_hp.change_resource_by_perc(1.0)
    print(f"{character.name} fully recovers HP.")


LATE_BLOOMER = PassiveEffect("Late Bloomer", description="On Turn 2, Fully recover HP",
                                    effect_function=late_bloomer, trigger_condition=effects.trigger_on_turn_x(2))

# Last Stance
def last_stance(character, battle):
    old_attack = character.attack.total
    character.attack.add_modifier(1.5, is_multiplicative=True)
    print(f"{character.name} ATK increased by 50%. {old_attack} -> {character.attack.total}")


LAST_STANCE = PassiveEffect("Last Stance", description="When HP is below 50%. Increase ATK by 50%", effect_function=last_stance,
                                   trigger_condition=effects.trigger_on_stat_threshold(lambda character: character.max_hp.get_percentage() < 0.5))

# Wolf Hunger
def wolf_hunger(character, battle):
    for ally in battle.get_character_allies(character):
        old_attack = ally.attack.total
        ally.attack.add_modifier(1.5, is_multiplicative=True)
        print(f"{ally.name} ATK increased by 50%. {old_attack} -> {ally.attack.total}")


WOLF_HUNGER = PassiveEffect("Wolf Hunger", description="When killed by an enemy. Increase allies ATK by 50%",
                                   effect_function=wolf_hunger, trigger_condition=effects.trigger_on_death_by_enemy)

# Burning Adrenaline
def burning_adrenaline(character, battle):
    old_crit_chance = character.crit_chance.total
    character.crit_chance.add_modifier(0.03)
    print(f"{character.name} CRIT CHANCE increased by 3% {old_crit_chance * 100}% -> {character.crit_chance.total * 100}%")


BURNING_ADRENALINE = PassiveEffect("Burning Adrenaline", description="+3% Crit Chance",
                                          effect_function=burning_adrenaline, trigger_condition=effects.trigger_on_start_of_battle)
# Harden
def harden(character, battle):
    old_res = character.resistance.total
    character.resistance.add_modifier(1.03, is_multiplicative=True)
    print(f"{character.name} RES increased by 3% {old_res} -> {character.resistance.total}")


HARDEN = PassiveEffect("Harden", description="+3% Resistance",
                              effect_function=harden, trigger_condition=effects.trigger_on_start_of_battle)

# Flowing Ring
def flowing_ring(character, battle):
    old_hp = character.max_hp.total
    character.max_hp.add_modifier(1.03, is_multiplicative=True)
    print(f"{character.name} MAXHP increased by 3% {old_hp} -> {character.max_hp.total}")


FLOWING_RING = PassiveEffect("Flowing Ring", description="+3% MAXHP",
                                    effect_function=flowing_ring, trigger_condition=effects.trigger_on_start_of_battle)

# Quick Boots
def quick_boots(character, battle):
    old_spd = character.speed.total
    character.speed.add_modifier(1.03, is_multiplicative=True)
    print(f"{character.name} SPD increased by 3% {old_spd} -> {character.speed.total}")


QUICK_BOOTS = PassiveEffect("Quick Boots", description="+3% SPD",
                                   effect_function=quick_boots, trigger_condition=effects.trigger_on_start_of_battle)

# Early Feast
def early_feast(character, battle):
    old_atk = character.attack.total
    old_crit_chance = character.crit_chance.total
    character.attack.add_modifier(1.5, is_multiplicative=True)
    character.crit_chance.add_modifier(0.5)
    print(f"{character.name} ATK increased by 50% {old_atk} -> {character.attack.total}")
    print(f"{character.name} CRIT CHANCE increased by 50% {old_crit_chance * 100}% -> {character.crit_chance.total * 100}%")


EARLY_FEAST = PassiveEffect("Early Feast", description="At the start of battle, Increase ATK and Crit Chance by 50% for 2 turns",
                                   effect_function=early_feast, trigger_condition=effects.trigger_on_start_of_battle)

# Demon Hunger
def demon_hunger(character, battle):
    old_attack = character.attack.total
    character.attack.add_modifier(1.2, is_multiplicative=True)
    print(f"{character.name} ATK increased by 20%. {old_attack} -> {character.attack.total}")


DEMON_HUNGER = PassiveEffect("Demon Hunger", description="Before attacking, if the target is a 'Demon', Increase ATK by 10% and inflict burn on the target.",
                                   effect_function=demon_hunger, trigger_condition=effects.trigger_on_attack)

# Death Will Arrive
def death_will_arrive(character, battle):
    for enemy in battle.get_character_enemies(character):
        if not (enemy.is_alive()):
            old_attack = character.attack.total
            character.attack.add_modifier(1.2, is_multiplicative=True)
            print(
                f"{character.name} ATK increased by 20%. {old_attack} -> {character.attack.total}")


DEATH_WILL_ARRIVE = PassiveEffect("Death Will Arrive", description="After attacking, if the target is dead, increase ATK by 20% of the target's ATK",
                                         effect_function=death_will_arrive, trigger_condition=effects.trigger_on_attack)
