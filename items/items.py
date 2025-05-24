import random

class BaseItem:
    def __init__(self, name: str, description: str = "", effect=None):
        self.name = name
        self.description = description
        self.effect = effect

    def __repr__(self) -> str:
        return f"{self.name}: {self.description}"


class Item:
    def __init__(self, item: BaseItem, quantity: int):
        self.item = item
        self.name = item.name
        self.quantity = quantity

    def __repr__(self) -> str:
        return f"{self.item.name} (x{self.quantity})"
    
    def __add__(self, other):
        if isinstance(other, Item) and self.item.name == other.item.name:
            return Item(self.item, self.quantity + other.quantity)
        raise ValueError("Cannot add different items together")


class LootTable:
    def __init__(self, items: list[(BaseItem, int, int, int)], amount_min: int, amount_max: int):
        self.items = items
        self.total_weight = sum(item[-1] for item in items)
        self.amount_min = amount_min
        self.amount_max = amount_max

    def generate_loot(self):
        loot = []
        for _ in range(random.randint(self.amount_min, self.amount_max)):
            item_base = random.choice(self.items, weights=[item[-1] for item in self.items])
            item = Item(item_base[0], random.randint(item_base[1], item_base[2]))
            loot.append(item)
        return loot

    def __repr__(self):
        toReturn = "LootTable("
        for item, weight in self.items:
            toReturn += f"{item.name}: {(weight/self.total_weight):.2f}%, "
        toReturn += ")"
        return toReturn
