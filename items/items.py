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


class LootTable:
    def __init__(self, items: list[(Item, int)], amount_min: int, amount_max: int):
        self.items = items
        self.total_weight = sum(weight for _, weight in items)
        self.amount_min = amount_min
        self.amount_max = amount_max

    def generate_loot(self):
        loot = []
        for _ in range(random.randint(self.amount_min, self.amount_max)):
            rand_num = random.randint(1, self.total_weight)
            current_weight = 0
            for item, weight in self.items:
                current_weight += weight
                if rand_num <= current_weight:
                    loot.append(item)
                    break
        return loot

    def __repr__(self):
        toReturn = "LootTable("
        for item, weight in self.items:
            toReturn += f"{item.name}: {(weight/self.total_weight):.2f}%, "
        toReturn += ")"
        return toReturn
