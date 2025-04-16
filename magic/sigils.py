from magic.runes import Rune

class Sigil:
    def __init__(self, name, rune_composition: list[Rune], description="", active_effects=[], passive_effects=[], equipped_character=None):
        self.name = name
        self.rune_composition = rune_composition
        self.description = description
        self.active_effects = active_effects
        self.passive_effects = passive_effects
        self.equipped_character = equipped_character

    def add_rune(self, rune):
        self.rune_composition.append(rune)

    def add_active_effect(self, active_effect):
        self.active_effects.append(active_effect)

    def add_passive_effect(self, passive_effect):
        self.passive_effects.append(passive_effect)

    def __repr__(self):
        return f"Sigil({self.name} {(i for i in self.rune_composition)} | ActiveEffects: {len(self.active_effects)}| PassiveEffects: {len(self.passive_effects)})"


