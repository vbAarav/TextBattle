<<<<<<< HEAD
<<<<<<< HEAD
from effect.passive.passive_effect import PassiveEffect
from effect.effects import ComplexEffect
=======
from effect.passive.passive_effect import PassiveEffect, ComplexEffect
>>>>>>> 6c35bee (Improved Passive Effect Architecture to Handle Larger Effects)
=======
from effect.passive.passive_effect import PassiveEffect
from effect.effects import ComplexEffect
>>>>>>> 02eaa78 (Improved Status Effect Architecture to Handle Larger Effects)
import effect.effects as effects


# Thousand Divine Cuts
def thousand_divine_cuts(character, battle, **kwargs):
    for enemy in battle.get_character_enemies(character):
        old_defense = enemy.defense.total
        enemy.defense.add_modifier(0.95, is_multiplicative=True)
        print(f"{enemy.name} DEF reduced by 5% {old_defense} -> {enemy.defense.total}")

<<<<<<< HEAD
<<<<<<< HEAD
THOUSAND_DIVINE_CUTS = PassiveEffect("Thousand Divine Cuts", description="At the start of battle, Decrease all enemies DEF by 5%",
=======
THOUSAND_DIVINE_CUTS = PassiveEffect("Thousand Divine Cuts", description="At the start of battle, All enemies have DEF reduced by 5%",
>>>>>>> 6c35bee (Improved Passive Effect Architecture to Handle Larger Effects)
=======
THOUSAND_DIVINE_CUTS = PassiveEffect("Thousand Divine Cuts", description="At the start of battle, Decrease all enemies DEF by 5%",
>>>>>>> e966423 (Implement Evasion, Accuracy and Better Speed Mechanic)
                                     effects=[ComplexEffect(effects.trigger_on_start_of_battle, thousand_divine_cuts)])

# Early Stance
def early_stance(character, battle, **kwargs):
    old_defense = character.defense.total
    character.defense.add_modifier(1.2, is_multiplicative=True)
    print(f"{character.name} DEF increased by 20%. {old_defense} -> {character.defense.total}")
    
def early_stance_remove(character, battle, **kwargs):
    old_defense = character.defense.total
    character.defense.remove_modifier(1.2, is_multiplicative=True)
    print(f"{character.name} DEF decreased by 20%. {old_defense} -> {character.defense.total}")
    
EARLY_STANCE = PassiveEffect("Early Stance", description="At the start of battle, Increase DEF by 20% for 5 turns", 
                             effects=[ComplexEffect(effects.trigger_on_start_of_battle, early_stance, max_duration=5, remove_effect=early_stance_remove)])

# Engine
def engine(character, battle, **kwargs):
    old_speed = character.speed.total
    character.speed.add_modifier(1)
    print(f"{character.name} SPD increased by 1. {old_speed} -> {character.speed.total}")


ENGINE = PassiveEffect("Engine", description="After receiving an attack, SPD + 1",
                       effects=[ComplexEffect(effects.trigger_after_receive_attack, engine)])

# Double Up
def double_up(character, battle, **kwargs):
    old_attack = character.attack.total
    character.attack.add_modifier(1.03, is_multiplicative=True)
    print(f"{character.name} ATK increased by 3%. {old_attack} -> {character.attack.total}")

DOUBLE_UP = PassiveEffect("Double Up", description="After executing an attack, Increase ATK by 3%",
                          effects=[ComplexEffect(effects.trigger_after_attack, double_up)])

# Late Bloomer
def late_bloomer(character, battle, **kwargs):
    old_hp = character.max_hp.total
    character.max_hp.change_resource_by_perc(0.05)
    print(f"{character.name} HP increased by 5%. {old_hp} -> {character.max_hp.total}")

LATE_BLOOMER = PassiveEffect("Late Bloomer", description="At the start of turn 2, Increase HP by 5%",
                             effects=[ComplexEffect(effects.trigger_on_turn_x(2), late_bloomer)])

# Last Stance
def last_stance(character, battle, **kwargs):
    old_attack = character.attack.total
    character.attack.add_modifier(1.5, is_multiplicative=True)
    print(f"{character.name} ATK increased by 50%. {old_attack} -> {character.attack.total}")

LAST_STANCE = PassiveEffect("Last Stance", description="The first time HP is below 50%. Increase ATK by 50%",
                            effects=[ComplexEffect(effects.trigger_on_stat_threshold(lambda character: character.max_hp.get_percentage() < 0.5), last_stance, max_stack=1)])

# Wolf Hunger
def wolf_hunger(character, battle, **kwargs):
    for ally in battle.get_character_allies(character):
        old_attack = ally.attack.total
        ally.attack.add_modifier(1.5, is_multiplicative=True)
        print(f"{ally.name} ATK increased by 50%. {old_attack} -> {ally.attack.total}")

WOLF_HUNGER = PassiveEffect("Wolf Hunger", description="When killed by an enemy. Increase allies ATK by 50%",
                            effects=[ComplexEffect(effects.trigger_on_death_by_enemy, wolf_hunger)])


# Burning Adrenaline
def burning_adrenaline(character, battle, **kwargs):
    old_crit_chance = character.crit_chance.total
    character.crit_chance.add_modifier(0.03)
    print(f"{character.name} CRIT CHANCE increased by 3% {old_crit_chance * 100}% -> {character.crit_chance.total * 100}%")


BURNING_ADRENALINE = PassiveEffect("Burning Adrenaline", description="At the start of battle, Increase Crit Chance by 3%",
                                   effects=[ComplexEffect(effects.trigger_on_start_of_battle, burning_adrenaline)])

# Harden
def harden(character, battle, **kwargs):
    old_res = character.resistance.total
    character.resistance.add_modifier(1.03, is_multiplicative=True)
    print(f"{character.name} RES increased by 3% {old_res} -> {character.resistance.total}")


HARDEN = PassiveEffect("Harden", description="At the start of battle, Increase Resistance by 3%",
                       effects=[ComplexEffect(effects.trigger_on_start_of_battle, harden)])

# Flowing Ring
def flowing_ring(character, battle, **kwargs):
    old_hp = character.max_hp.total
    character.max_hp.add_modifier(1.03, is_multiplicative=True)
    print(f"{character.name} MAXHP increased by 3% {old_hp} -> {character.max_hp.total}")


FLOWING_RING = PassiveEffect("Flowing Ring", description="At the start of battle, Increase MAXHP by 3%",
                             effects=[ComplexEffect(effects.trigger_on_start_of_battle, flowing_ring)])

# Quick Boots
def quick_boots(character, battle, **kwargs):
    old_spd = character.speed.total
    character.speed.add_modifier(1.03, is_multiplicative=True)
    print(f"{character.name} SPD increased by 3% {old_spd} -> {character.speed.total}")


QUICK_BOOTS = PassiveEffect("Quick Boots", description="At the start of battle, Increase SPD by 3%",
                            effects=[ComplexEffect(effects.trigger_on_start_of_battle, quick_boots)])


# Early Feast
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


EARLY_FEAST = PassiveEffect("Early Feast", description="At the start of battle, Increase ATK and Crit Chance by 50% for 2 turns",
                            effects=[ComplexEffect(effects.trigger_on_start_of_battle, early_feast, remove_effect=early_feast_remove, max_duration=2)])

# Demon Hunger
def demon_hunger(character, battle, **kwargs):
    old_attack = character.attack.total
    character.attack.add_modifier(1.2, is_multiplicative=True)
    print(f"{character.name} ATK increased by 20%. {old_attack} -> {character.attack.total}")


DEMON_HUNGER = PassiveEffect("Demon Hunger", description="Before executing an attack, if the target is a 'Demon', Increase ATK by 10% and inflict burn on the target.",
                             effects=[ComplexEffect(effects.trigger_before_attack, demon_hunger, 
                            condition=lambda character, battle, **kwargs: kwargs.get("target").race and kwargs.get("target").race == "Demon")])
                            

# Death Will Arrive
def death_will_arrive(character, battle, **kwargs):
    for enemy in battle.get_character_enemies(character):
        if not (enemy.is_alive()):
            old_attack = character.attack.total
            character.attack.add_modifier(1.2, is_multiplicative=True)
            print(f"{character.name} ATK increased by 20%. {old_attack} -> {character.attack.total}")


DEATH_WILL_ARRIVE = PassiveEffect("Death Will Arrive", description="After executing an attack, if the target is dead, increase ATK by 20% of the target's ATK",
                                  effects=[ComplexEffect(effects.trigger_after_attack, death_will_arrive, 
                                  condition=lambda character, battle, **kwargs: kwargs.get("target").is_alive() == False)])

# Glowing Aura
def glowing_aura(character, battle, **kwargs):
    old_evasion = character.evasion.total
    character.evasion.add_modifier(1.03, is_multiplicative=True)
    print(f"{character.name} EV increased by 3% {old_evasion} -> {character.evasion.total}")
    
GLOWING_AURA = PassiveEffect("Glowing Aura", description="At the start of battle, Increase Evasion by 3%",
                             effects=[ComplexEffect(effects.trigger_on_start_of_battle, glowing_aura)])
    
# Embrace the Darkness
def embrace_the_darkness_one(character, battle, **kwargs):
    old_spd = character.speed.total
    character.speed.add_modifier(1.05, is_multiplicative=True)
    print(f"{character.name} SPD increased by 5% {old_spd} -> {character.speed.total}")
    
def embrace_the_darkness_two(character, battle, **kwargs):
    old_spd = character.speed.total
    character.speed.add_modifier(1.2, is_multiplicative=True)
    print(f"{character.name} SPD increased by 20% {old_spd} -> {character.speed.total}")

EMBRACE_THE_DARKNESS = PassiveEffect("Embrace the Darkness", description="At the start of battle, Increase SPD by 5%. The first time HP is below 20%, Increase SPD by 20%.",
                       effects=[ComplexEffect(effects.trigger_on_start_of_battle, embrace_the_darkness_one), 
                       ComplexEffect(effects.trigger_on_stat_threshold(lambda character: character.max_hp.get_percentage() < 0.2), embrace_the_darkness_two, max_stack=1)])
    