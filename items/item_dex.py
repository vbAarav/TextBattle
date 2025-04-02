from items.items import BaseItem

# Items
GOLD = BaseItem("Gold")
SILVER = BaseItem("Silver")
BRONZE = BaseItem("Bronze")
SLIME_ESSENCE = BaseItem("Slime Essence")

# Complex Items
MINT_HERB = BaseItem("Mint Herb", "Increase HP by 10. 10% chance to remove all status conditions.")
LIFE_HEART = BaseItem("Life Heart", "Increase all allies Crit Chance by 50% and inflict poison on all allies.")
GAMBLE_HEART = BaseItem("Gamble of the Heart", "Set the target's HP to a random amount")