from character.characters import Character, Colour
import magic.rune_archive as rune_archive

# Characters
RED_SLIME = Character(
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

RED_MAGIC_SLIME = Character(
    name="Red Magic Slime",
    type=Colour.RED,
    max_hp=80,
    attack=3,
    defense=2,
    speed=1,
    description="""
        A sentient collection of magical liquid.
    """,
    runes=[rune_archive.FIRE]
)

BLUE_SLIME = Character(
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

BLUE_MAGIC_SLIME = Character(
    name="Blue Magic Slime",
    type=Colour.BLUE,
    max_hp=80,
    attack=3,
    defense=2,
    speed=1,
    description="""
        A sentient collection of magical liquid.
    """,
    runes=[rune_archive.WATER]
)

GREEN_SLIME = Character(
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

GREEN_MAGIC_SLIME = Character(
    name="Green Magic Slime",
    type=Colour.GREEN,
    max_hp=80,
    attack=3,
    defense=2,
    speed=1,
    description="""
        A sentient collection of magical liquid.
    """,
    runes=[rune_archive.WIND]
)

ROCK_GOLEM = Character(
    name="Rock Golem",
    max_hp=50,
    attack=6,
    defense=10,
    speed=10,
    runes=[rune_archive.ROCK]
)

STORM_HAWK = Character(
    name="Storm Hawk",
    type=Colour.BLUE,
    max_hp=30,
    attack=5,
    defense=3,
    speed=8,
    runes=[rune_archive.BLUE_LIGHTNING]
)

DEEP_SEA_SNAKE = Character(
    name="Deep Sea Snake",
    type=Colour.BLUE,
    max_hp=40,
    attack=7,
    defense=5,
    speed=3,
    runes=[rune_archive.WATER]
)

AZELGRAM = Character(
    name="Azelgram",
    max_hp=100,
    attack=10,
    defense=10,
    speed=10,
    runes=[rune_archive.PURPLE_POWER, rune_archive.GRIM_CORPSE],
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