from magic.sigils import Sigil
import magic.runes as runes
import effect.active_effects as active_effects
import effect.passive_effects as passive_effects


# Sigils
FIRE = Sigil(
    name="Fire",
    tier=1,
    rune_composition={runes.FIRE: 2},
    active_effects=[active_effects.RUNE_FORCE],
    passive_effects=[passive_effects.BURNING_ADRENALINE]
)

WATER = Sigil(
    name="Water",
    tier=1,
    rune_composition={runes.WATER: 2},
    active_effects=[active_effects.RUNE_FORCE],
    passive_effects=[passive_effects.FLOWING_RING]
)

EARTH = Sigil(
    name="Earth",
    tier=1,
    rune_composition={runes.EARTH: 2},
    active_effects=[active_effects.RUNE_FORCE],
    passive_effects=[passive_effects.HARDEN]
)

WIND = Sigil(
    name="Wind",
    tier=1,
    rune_composition={runes.WIND: 2},
    active_effects=[active_effects.RUNE_FORCE],
    passive_effects=[passive_effects.QUICK_BOOTS]
)

DARK = Sigil(
    name="Dark",
    tier=1,
    rune_composition={runes.DARK: 2},
    active_effects=[active_effects.RUNE_FORCE],
    passive_effects=[passive_effects.QUICK_BOOTS]
)

LIGHT = Sigil(
    name="Light",
    tier=1,
    rune_composition={runes.LIGHT: 2},
    active_effects=[active_effects.RUNE_FORCE],
    passive_effects=[passive_effects.QUICK_BOOTS]
)

ICE = Sigil(
    name="Ice",
    tier=1,
    rune_composition={runes.ICE: 2},
    active_effects=[active_effects.RUNE_FORCE],
    passive_effects=[passive_effects.QUICK_BOOTS]
)

GRASS = Sigil(
    name="Grass",
    tier=1,
    rune_composition={runes.GRASS: 2},
    active_effects=[active_effects.RUNE_FORCE],
    passive_effects=[passive_effects.QUICK_BOOTS]
)

SPACE = Sigil(
    name="Space",
    tier=1,
    rune_composition={runes.SPACE: 2},
    active_effects=[active_effects.RUNE_FORCE],
    passive_effects=[passive_effects.QUICK_BOOTS]
)

FLOWING_STEAM = Sigil(
    name="Flowing Steam",
    tier=2,
    rune_composition={runes.FIRE: 2, runes.WATER: 2},
    active_effects=[active_effects.RUNE_FORCE],
    passive_effects=[]
)

MOLTEN_LAVA = Sigil(
    name="Molten Lava",
    tier=2,
    rune_composition={runes.FIRE: 2, runes.EARTH: 2},
    active_effects=[active_effects.RUNE_FORCE],
    passive_effects=[]
)

BURNING_AIR = Sigil(
    name="Burning Air",
    tier=2,
    rune_composition={runes.FIRE: 2, runes.WIND: 2},
    active_effects=[active_effects.RUNE_FORCE],
    passive_effects=[]
)

AQUATIC_EROSION = Sigil(
    name="Aquatic Erosion",
    tier=2,
    rune_composition={runes.WATER: 2, runes.EARTH: 2},
    active_effects=[active_effects.RUNE_FORCE],
    passive_effects=[]
)

CRYSTALISED_ICE = Sigil(
    name="Crystalised Ice",
    tier=2,
    rune_composition={runes.ICE: 2, runes.EARTH: 2},
    active_effects=[active_effects.RUNE_FORCE, active_effects.GUARD_SWITCH]
)

GLOWING_GRASS = Sigil(
    name="Glowing Grass",
    tier=2,
    rune_composition={runes.LIGHT: 2, runes.GRASS: 2},
    active_effects=[active_effects.RUNE_FORCE]
)

BLUE_LIGHTNING = Sigil(
    name="Blue Lightning",
    tier=2,
    rune_composition={runes.ELECTRIC: 3, runes.WATER: 1},
    active_effects=[active_effects.EVASIVE_AGILITY, active_effects.GALE_LIGHTNING]
)

LESSER_LIGHT = Sigil(
    name="Lesser Light",
    tier=2,
    rune_composition={runes.DARK: 1, runes.LIGHT: 3},
    active_effects=[active_effects.RUNE_FORCE],
    passive_effects=[passive_effects.GLOWING_AURA]
)

SHADOW_WIND = Sigil(
    name="Shadow Wind",
    tier=2,
    rune_composition={runes.DARK: 2, runes.WIND: 2},
    active_effects=[active_effects.RUNE_FORCE],
    passive_effects=[passive_effects.EMBRACE_THE_DARKNESS]
)

PURPLE_POWER = Sigil(
    name="Purple Power",
    tier=2,
    rune_composition={runes.DARK: 4},
    active_effects=[active_effects.RUNE_FORCE, active_effects.UNSTABLE_STRENGTH],
    passive_effects=[passive_effects.EARLY_FEAST, passive_effects.DEMON_HUNGER]
)

GRIM_CORPSE = Sigil(
    name="Grim Corpse",
    tier=2,
    rune_composition={runes.DARK: 4},
    active_effects=[active_effects.RUNE_FORCE, active_effects.DARK_PIT],
    passive_effects=[passive_effects.DEATH_WILL_ARRIVE]
)