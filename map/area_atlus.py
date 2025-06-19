import character.character_archive as character_archive
import items.loot_tables as loot_tables
from map.location import Area
import copy

# Long Plains
LONG_PLAINS = Area(
    "Long Plains",
    enemies={
        copy.deepcopy(character_archive.RED_SLIME): (2, loot_tables.SLIME_DEATH),
        copy.deepcopy(character_archive.RED_MAGIC_SLIME): (1, loot_tables.SLIME_DEATH),
        copy.deepcopy(character_archive.BLUE_SLIME): (2, loot_tables.SLIME_DEATH),
        copy.deepcopy(character_archive.BLUE_MAGIC_SLIME): (1, loot_tables.SLIME_DEATH),
        copy.deepcopy(character_archive.GREEN_SLIME): (2, loot_tables.SLIME_DEATH),
        copy.deepcopy(character_archive.GREEN_MAGIC_SLIME): (1, loot_tables.SLIME_DEATH)
    }
)
