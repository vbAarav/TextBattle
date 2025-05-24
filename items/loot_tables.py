from items.items import Item, LootTable
import items.item_dex as item_dex

# Loot
SLIME_DEATH = LootTable(
    items=[(item_dex.GOLD, 1, 2, 20), (item_dex.SILVER, 1, 6, 30), (item_dex.BRONZE, 1, 40, 50),(item_dex.SLIME_ESSENCE, 3, 10)],
    amount_min=1, amount_max=3
)