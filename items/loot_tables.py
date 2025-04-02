from items.items import Item, LootTable
import items.item_dex as item_dex

# Loot
SLIME_DEATH = LootTable(
    items=[(Item(item_dex.GOLD, 1), 20), (Item(item_dex.SILVER, 6), 30), (Item(item_dex.BRONZE, 40), 50),
           (Item(item_dex.SLIME_ESSENCE, 3), 10)],
    amount_min=1, amount_max=3
)