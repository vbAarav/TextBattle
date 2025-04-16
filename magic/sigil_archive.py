from magic.sigils import Sigil
import effect.active_effects as active_effects
import effect.passive.effects as passive_effects

# Runes
POWER = Sigil(
    name="Power",
    active_effects=[active_effects.RUNE_FORCE, active_effects.LARGE_SLICE,
                    active_effects.ENFORCED_VIGOR, active_effects.GUARD_SWITCH, active_effects.HEAL_ALL],
    passive_effects=[passive_effects.THOUSAND_DIVINE_CUTS, passive_effects.EARLY_STANCE, passive_effects.DOUBLE_UP,
                     passive_effects.ENGINE, passive_effects.LATE_BLOOMER, passive_effects.LAST_STANCE, passive_effects.WOLF_HUNGER]
)

FIRE = Sigil(
    name="Fire",
    active_effects=[active_effects.RUNE_FORCE],
    passive_effects=[passive_effects.BURNING_ADRENALINE]
)

WATER = Sigil(
    name="Water",
    active_effects=[active_effects.RUNE_FORCE],
    passive_effects=[passive_effects.FLOWING_RING]
)

EARTH = Sigil(
    name="Earth",
    active_effects=[active_effects.RUNE_FORCE],
    passive_effects=[passive_effects.HARDEN]
)

WIND = Sigil(
    name="Wind",
    active_effects=[active_effects.RUNE_FORCE],
    passive_effects=[passive_effects.QUICK_BOOTS]
)

ROCK = Sigil(
    name="Rock",
    active_effects=[active_effects.RUNE_FORCE, active_effects.POLISH]
)

CRYSTALISED_ICE = Sigil(
    name="Crystalised Ice",
    active_effects=[active_effects.RUNE_FORCE, active_effects.GUARD_SWITCH]
)

GLOWING_GRASS = Sigil(
    name="Glowing Grass",
    active_effects=[active_effects.RUNE_FORCE, active_effects.HEAL_ALL]
)

BLUE_LIGHTNING = Sigil(
    name="Blue Lightning",
    active_effects=[active_effects.EVASIVE_AGILITY, active_effects.GALE_LIGHTNING]
)

LESSER_LIGHT = Sigil(
    name="Lesser Light",
    active_effects=[active_effects.RUNE_FORCE],
    passive_effects=[passive_effects.GLOWING_AURA]
)

SHADOW_WIND = Sigil(
    name="Shadow Wind",
    active_effects=[active_effects.RUNE_FORCE],
    passive_effects=[passive_effects.EMBRACE_THE_DARKNESS]
)

PURPLE_POWER = Sigil(
    name="Purple Power",
    active_effects=[active_effects.RUNE_FORCE, active_effects.UNSTABLE_STRENGTH],
    passive_effects=[passive_effects.EARLY_FEAST, passive_effects.DEMON_HUNGER]
)

GRIM_CORPSE = Sigil(
    name="Grim Corpse",
    active_effects=[active_effects.RUNE_FORCE, active_effects.DARK_PIT],
    passive_effects=[passive_effects.DEATH_WILL_ARRIVE]
)