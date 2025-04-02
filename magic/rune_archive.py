from magic.runes import Rune
import effect.active_effects as active_effects
import effect.passive_effects as passive_effects

# Runes
POWER = Rune(
    name="Power",
    active_effects=[active_effects.RUNE_FORCE, active_effects.LARGE_SLICE,
                    active_effects.ENFORCED_VIGOR, active_effects.GUARD_SWITCH, active_effects.HEAL_ALL],
    passive_effects=[passive_effects.THOUSAND_DIVINE_CUTS, passive_effects.EARLY_STANCE, passive_effects.DOUBLE_UP,
                     passive_effects.ENGINE, passive_effects.LATE_BLOOMER, passive_effects.LAST_STANCE, passive_effects.WOLF_HUNGER]
)

FIRE = Rune(
    name="Fire",
    active_effects=[active_effects.RUNE_FORCE],
    passive_effects=[passive_effects.BURNING_ADRENALINE]
)

WATER = Rune(
    name="Water",
    active_effects=[active_effects.RUNE_FORCE],
    passive_effects=[passive_effects.FLOWING_RING]
)

EARTH = Rune(
    name="Earth",
    active_effects=[active_effects.RUNE_FORCE],
    passive_effects=[passive_effects.HARDEN]
)

WIND = Rune(
    name="Wind",
    active_effects=[active_effects.RUNE_FORCE],
    passive_effects=[passive_effects.QUICK_BOOTS]
)

ROCK = Rune(
    name="Rock",
    active_effects=[active_effects.RUNE_FORCE, active_effects.POLISH]
)

CRYSTALISED_ICE = Rune(
    name="Crystalised Ice",
    active_effects=[active_effects.RUNE_FORCE, active_effects.GUARD_SWITCH]
)

GLOWING_GRASS = Rune(
    name="Glowing Grass",
    active_effects=[active_effects.RUNE_FORCE, active_effects.HEAL_ALL]
)

BLUE_LIGHTNING = Rune(
    name="Blue Lightning",
    active_effects=[active_effects.EVASIVE_AGILITY, active_effects.GALE_LIGHTNING]
)

PURPLE_POWER = Rune(
    name="Purple Power",
    active_effects=[active_effects.RUNE_FORCE, active_effects.UNSTABLE_STRENGTH],
    passive_effects=[passive_effects.EARLY_FEAST, passive_effects.DEMON_HUNGER]
)

GRIM_CORPSE = Rune(
    name="Grim Corpse",
    active_effects=[active_effects.RUNE_FORCE, active_effects.DARK_PIT],
    passive_effects=[passive_effects.DEATH_WILL_ARRIVE]
)