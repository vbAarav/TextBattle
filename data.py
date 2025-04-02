from characters import Character, Colour, Damage
from runes import Rune
from effects import ActiveEffect, PassiveEffect, StatusEffect
import effects
import random
import time
import items
import map


# Active Effects
def rune_force(character, battle):
    target = battle.choose_target(battle.get_all_characters(), character)
    if target:
        print(f"{character.name} attacks {target.name}!")
        multiplier = 1.2
        damage = Damage()
        damage.build(max(character.attack.total + 1,
                     int(character.attack.total * multiplier)), character, target)
        target.receive_attack(damage, character, battle)
        time.sleep(1)


effect_rune_force = ActiveEffect(
    "Rune Force", description="Attacks the target. Dealing 120% of ATK as Damage", effect_function=rune_force)


def large_slice(character, battle):
    target = battle.choose_target(battle.get_all_characters(), character)
    if target:
        print(f"{character.name} attacks {target.name}!")
        multiplier = random.uniform(1.0, 1.5)
        damage = Damage()
        damage.build(max(character.attack.total + 1,
                     int(character.attack.total * multiplier)), character, target)
        target.receive_attack(damage, character, battle)
        time.sleep(1)


effect_large_slice = ActiveEffect(
    "Large Slice", description="Attacks the target. Dealing (100% - 150%) of ATK as Damage", effect_function=large_slice)


def heal_all_allies(character, battle):
    for ally in battle.get_character_allies(character):
        heal_amount = max(1, ally.max_hp.total * 0.05)
        ally.receive_heal(heal_amount)
        time.sleep(1)


effect_heal_all = ActiveEffect(
    "Heal All", description="All allies heal health equal to 5% of MAXHP", effect_function=heal_all_allies)


def swap_atk_def(character, battle):
    character.attack, character.defense = character.defense, character.attack
    character.attack.name, character.defense.name = character.defense.name, character.attack.name
    print(f"{character.name} swapped ATK and DEF stats.")
    time.sleep(1)


effect_guard_switch = ActiveEffect(
    "Guard Switch", description="Swaps the character's ATK and DEF Stats", effect_function=swap_atk_def)


def damage_ally_and_poison_enemy(character, battle):
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
        random_enemy.add_status_effect(effect_status_poison)

    else:
        # Deal Damage
        print(f"{character.name} attacks {target.name}!")
        damage = Damage()
        damage.build(int(character.attack.total * 0.5), character, target)
        target.receive_attack(damage, character, battle)


effect_enforced_vigor = ActiveEffect(
    "Enforced Vigor", description="Attacks the target. Dealing 50% of ATK as Damage. If the target is an ally. Attacks the target. Dealing 180% of ATK as Damage and poison a random enemy for 3 turns.",
    effect_function=damage_ally_and_poison_enemy)


def polish(character, battle):
    for target in battle.get_character_allies(character):
        old_defense = target.defense.total
        target.defense.add_modifier(1.05, is_multiplicative=True)
        print(
            f"{target.name} DEF increased by 5% {old_defense} -> {target.defense.total}")


effect_polish = ActiveEffect(
    "Polish", description="Increases all allies DEF by 5% for 3 turns.",
    effect_function=polish
)


def gale_lightning(character, battle):
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


effect_gale_lightning = ActiveEffect(
    "Gale Lightning", description="Deals 100% ATK damage and increases its SPD by 10% for 2 turns.",
    effect_function=gale_lightning
)


def evasive_agility(character, battle):
    old_evasion = character.evasion.total
    character.evasion.add_modifier(1.15, is_multiplicative=True)
    print(f"{character.name} EV increased by 10% {old_evasion} -> {character.evasion.total}")


effect_evasive_agility = ActiveEffect(
    "Evasive Agility", description="+15% Evasion for 3 turns.",
    effect_function=evasive_agility
)


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


effect_unstable_strength = ActiveEffect(
    "Unstable Strength", description="Deals (90 - 150)% ATK as Damage to the target. This attack ignores 20% of the target's DEF.",
    effect_function=unstable_strength)


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


effect_dark_pit = ActiveEffect(
    "Dark Pit", description="Deals 30% of ATK as Damage to all enemies. Increase multiplier by 50% for every dead character in battle.",
    effect_function=dark_pit)


# Passive Effects
def thousand_divine_cuts(character, battle):
    for enemy in battle.get_character_enemies(character):
        old_defense = enemy.defense.total
        enemy.defense.add_modifier(0.95, is_multiplicative=True)
        print(f"{enemy.name} DEF reduced by 5% {old_defense} -> {enemy.defense.total}")


effect_thousand_divine_cuts = PassiveEffect("Thousand Divine Cuts", description="At the start of battle, All enemies have DEF reduced by 5%",
                                            effect_function=thousand_divine_cuts, trigger_condition=effects.trigger_on_start_of_battle)


def early_stance(character, battle):
    old_defense = character.defense.total
    character.defense.add_modifier(1.2, is_multiplicative=True)
    print(f"{character.name} enters an early stance. DEF increased by 20%. {old_defense} -> {character.defense.total}")


effect_early_stance = PassiveEffect("Early Stance", description="For 5 turns, Increase DEF by 20%",
                                    effect_function=early_stance, trigger_condition=effects.trigger_within_first_x_turns(5))


def engine(character, battle):
    old_speed = character.speed.total
    character.speed.add_modifier(1)
    print(f"{character.name} SPD increased by 1. {old_speed} -> {character.speed.total}")


effect_engine = PassiveEffect("Engine", description="After receiving an attack, SPD + 1",
                              effect_function=engine, trigger_condition=effects.trigger_on_receive_attack)


def double_up(character, battle):
    old_attack = character.attack.total
    character.attack.add_modifier(1.03, is_multiplicative=True)
    print(f"{character.name} ATK increased by 3%. {old_attack} -> {character.attack.total}")


effect_double_up = PassiveEffect("Double Up", description="After executing an attack, Increase ATK by 3%",
                                 effect_function=double_up, trigger_condition=effects.trigger_on_attack)


def late_bloomer(character, battle):
    character.max_hp.change_resource_by_perc(1.0)
    print(f"{character.name} fully recovers HP.")


effect_late_bloomer = PassiveEffect("Late Bloomer", description="On Turn 2, Fully recover HP",
                                    effect_function=late_bloomer, trigger_condition=effects.trigger_on_turn_x(2))


def last_stance(character, battle):
    old_attack = character.attack.total
    character.attack.add_modifier(1.5, is_multiplicative=True)
    print(f"{character.name} ATK increased by 50%. {old_attack} -> {character.attack.total}")


effect_last_stance = PassiveEffect("Last Stance", description="When HP is below 50%. Increase ATK by 50%", effect_function=last_stance,
                                   trigger_condition=effects.trigger_on_stat_threshold(lambda character: character.max_hp.get_percentage() < 0.5))


def wolf_hunger(character, battle):
    for ally in battle.get_character_allies(character):
        old_attack = ally.attack.total
        ally.attack.add_modifier(1.5, is_multiplicative=True)
        print(f"{ally.name} ATK increased by 50%. {old_attack} -> {ally.attack.total}")


effect_wolf_hunger = PassiveEffect("Wolf Hunger", description="When killed by an enemy. Increase allies ATK by 50%",
                                   effect_function=wolf_hunger, trigger_condition=effects.trigger_on_death_by_enemy)


def burning_adrenaline(character, battle):
    old_crit_chance = character.crit_chance.total
    character.crit_chance.add_modifier(0.03)
    print(f"{character.name} CRIT CHANCE increased by 3% {old_crit_chance * 100}% -> {character.crit_chance.total * 100}%")


effect_burning_adrenaline = PassiveEffect("Burning Adrenaline", description="+3% Crit Chance",
                                          effect_function=burning_adrenaline, trigger_condition=effects.trigger_on_start_of_battle)


def harden(character, battle):
    old_res = character.resistance.total
    character.resistance.add_modifier(1.03, is_multiplicative=True)
    print(f"{character.name} RES increased by 3% {old_res} -> {character.resistance.total}")


effect_harden = PassiveEffect("Harden", description="+3% Resistance",
                              effect_function=harden, trigger_condition=effects.trigger_on_start_of_battle)


def flowing_ring(character, battle):
    old_hp = character.max_hp.total
    character.max_hp.add_modifier(1.03, is_multiplicative=True)
    print(f"{character.name} MAXHP increased by 3% {old_hp} -> {character.max_hp.total}")


effect_flowing_ring = PassiveEffect("Flowing Ring", description="+3% MAXHP",
                                    effect_function=flowing_ring, trigger_condition=effects.trigger_on_start_of_battle)


def quick_boots(character, battle):
    old_spd = character.speed.total
    character.speed.add_modifier(1.03, is_multiplicative=True)
    print(f"{character.name} SPD increased by 3% {old_spd} -> {character.speed.total}")


effect_quick_boots = PassiveEffect("Quick Boots", description="+3% SPD",
                                   effect_function=quick_boots, trigger_condition=effects.trigger_on_start_of_battle)


def early_feast(character, battle):
    old_atk = character.attack.total
    old_crit_chance = character.crit_chance.total
    character.attack.add_modifier(1.5, is_multiplicative=True)
    character.crit_chance.add_modifier(0.5)
    print(f"{character.name} ATK increased by 50% {old_atk} -> {character.attack.total}")
    print(f"{character.name} CC increased by 50% {old_crit_chance * 100}% -> {character.crit_chance.total * 100}%")


effect_early_feast = PassiveEffect("Early Feast", description="At the start of battle, Increase ATK and Crit Chance by 50% for 2 turns",
                                   effect_function=early_feast, trigger_condition=effects.trigger_on_start_of_battle)


def demon_hunger(character, battle):
    old_attack = character.attack.total
    character.attack.add_modifier(1.2, is_multiplicative=True)
    print(f"{character.name} ATK increased by 20%. {old_attack} -> {character.attack.total}")


effect_demon_hunger = PassiveEffect("Demon Hunger", description="Before attacking, if the target is a 'Demon', Increase ATK by 10% and inflict burn on the target.",
                                    effect_function=demon_hunger, trigger_condition=effects.trigger_on_attack)


def death_will_arrive(character, battle):
    for enemy in battle.get_character_enemies(character):
        if not (enemy.is_alive()):
            old_attack = character.attack.total
            character.attack.add_modifier(1.2, is_multiplicative=True)
            print(
                f"{character.name} ATK increased by 20%. {old_attack} -> {character.attack.total}")


effect_death_will_arrive = PassiveEffect("Death Will Arrive", description="After attacking, if the target is dead, increase ATK by 20% of the target's ATK",
                                         effect_function=death_will_arrive, trigger_condition=effects.trigger_on_attack)

# Status Effects


def poison(character, battle):
    damage = character.max_hp.total * 0.06
    print(f"{character.name} is poisoned")
    character.take_damage(damage, battle)


effect_status_poison = StatusEffect("Poison", description="Takes 6% of Max HP as damage at the start of turn",
                                    duration=3, ongoing_effect=poison, trigger_condition=effects.trigger_on_start_of_turn)


def stun(character, battle):
    print(f"{character.name} is stunned")


effect_status_stun = StatusEffect("Stun", description="Skips the character's turn", duration=1,
                                  ongoing_effect=stun, trigger_condition=effects.trigger_on_start_of_character_turn)


# Runes
power_rune = Rune(
    name="Power Rune",
    active_effects=[effect_rune_force, effect_large_slice,
                    effect_enforced_vigor, effect_guard_switch, effect_heal_all],
    passive_effects=[effect_thousand_divine_cuts, effect_early_stance, effect_double_up,
                     effect_engine, effect_late_bloomer, effect_last_stance, effect_wolf_hunger]
)

fire_rune = Rune(
    name="Fire Rune",
    active_effects=[effect_rune_force],
    passive_effects=[effect_burning_adrenaline]
)

water_rune = Rune(
    name="Water Rune",
    active_effects=[effect_rune_force],
    passive_effects=[effect_flowing_ring]
)

earth_rune = Rune(
    name="Earth Rune",
    active_effects=[effect_rune_force],
    passive_effects=[effect_harden]
)

wind_rune = Rune(
    name="Wind Rune",
    active_effects=[effect_rune_force],
    passive_effects=[effect_quick_boots]
)

rock_rune = Rune(
    name="Rock Rune",
    active_effects=[effect_rune_force, effect_polish]
)

crystalised_ice_rune = Rune(
    name="Crystalised Ice Rune",
    active_effects=[effect_rune_force, effect_guard_switch]
)

glowing_grass_rune = Rune(
    name="Glowing Grass Rune",
    active_effects=[effect_rune_force, effect_heal_all]
)

blue_lightning_rune = Rune(
    name="Blue Lightning Rune",
    active_effects=[effect_evasive_agility, effect_gale_lightning]
)

purple_power_rune = Rune(
    name="Purple Power Rune",
    active_effects=[effect_rune_force, effect_unstable_strength],
    passive_effects=[effect_early_feast, effect_demon_hunger]
)

grim_corpse_rune = Rune(
    name="Grim Corpse Rune",
    active_effects=[effect_rune_force, effect_dark_pit],
    passive_effects=[effect_death_will_arrive]
)


# Characters
chr_red_slime = Character(
    name="Red Slime",
    type=Colour.RED,
    max_hp=80,
    attack=2,
    defense=2,
    speed=1,
    description="""
        A sentient collection of magical liquid.
    """
)

chr_red_magic_slime = Character(
    name="Red Magic Slime",
    type=Colour.RED,
    max_hp=80,
    attack=3,
    defense=2,
    speed=1,
    description="""
        A sentient collection of magical liquid.
    """,
    runes=[fire_rune]
)

chr_blue_slime = Character(
    name="Blue Slime",
    type=Colour.BLUE,
    max_hp=80,
    attack=2,
    defense=2,
    speed=1,
    description="""
        A sentient collection of magical liquid.
    """
)

chr_blue_magic_slime = Character(
    name="Blue Magic Slime",
    type=Colour.BLUE,
    max_hp=80,
    attack=3,
    defense=2,
    speed=1,
    description="""
        A sentient collection of magical liquid.
    """,
    runes=[water_rune]
)

chr_green_slime = Character(
    name="Green Slime",
    type=Colour.GREEN,
    max_hp=80,
    attack=2,
    defense=2,
    speed=1,
    description="""
        A sentient collection of magical liquid.
    """
)

chr_green_magic_slime = Character(
    name="Green Magic Slime",
    type=Colour.GREEN,
    max_hp=80,
    attack=3,
    defense=2,
    speed=1,
    description="""
        A sentient collection of magical liquid.
    """,
    runes=[wind_rune]
)

chr_rock_golem = Character(
    name="Rock Golem",
    max_hp=50,
    attack=6,
    defense=10,
    speed=10,
    runes=[rock_rune]
)

chr_storm_hawk = Character(
    name="Storm Hawk",
    type=Colour.BLUE,
    max_hp=30,
    attack=5,
    defense=3,
    speed=8,
    runes=[blue_lightning_rune]
)

chr_deep_sea_snake = Character(
    name="Deep Sea Snake",
    type=Colour.BLUE,
    max_hp=40,
    attack=7,
    defense=5,
    speed=3,
    runes=[water_rune]
)

chr_azelgram = Character(
    name="Azelgram",
    max_hp=100,
    attack=10,
    defense=10,
    speed=10,
    runes=[purple_power_rune, grim_corpse_rune],
    description="""
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


# Items
gold = items.BaseItem("Gold")
silver = items.BaseItem("Silver")
bronze = items.BaseItem("Bronze")

slime_essence = items.BaseItem("Slime Essence")

mint_herb = items.BaseItem(
    "Mint Herb", "Increase HP by 10. 10% chance to remove all status conditions.")
life_heart = items.BaseItem(
    "Life Heart", "Increase all allies Crit Chance by 50% and inflict poison on all allies.")
gamble_heart = items.BaseItem(
    "Gamble of the Heart", "Set the target's HP to a random amount")

# Loot
slime_loot = items.LootTable(
    items=[(items.Item(gold, 1), 20), (items.Item(silver, 6), 30), (items.Item(bronze, 40), 50),
           (items.Item(slime_essence, 3), 10)],
    amount_min=1, amount_max=3
)


# Areas
area_long_plains = map.Area("Long Plains")
area_long_plains.add_enemy(chr_red_slime, 2, slime_loot)
area_long_plains.add_enemy(chr_red_magic_slime, 1, slime_loot)
area_long_plains.add_enemy(chr_blue_slime, 2, slime_loot)
area_long_plains.add_enemy(chr_blue_magic_slime, 1, slime_loot)
area_long_plains.add_enemy(chr_green_slime, 2, slime_loot)
area_long_plains.add_enemy(chr_green_magic_slime, 1, slime_loot)
