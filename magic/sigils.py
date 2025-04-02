
class Sigil:
    def __init__(self, name, description="", active_effects=[], passive_effects=[], equipped_character=None):
        self.name = name
        self.description = description
        self.active_effects = active_effects
        self.passive_effects = passive_effects
        self.equipped_character = equipped_character

    def add_active_effect(self, active_effect):
        self.active_effects.append(active_effect)

    def add_passive_effect(self, passive_effect):
        self.passive_effects.append(passive_effect)

    def __repr__(self):
        return f"Sigil({self.name}, ActiveEffects: {len(self.active_effects)}, PassiveEffects: {len(self.passive_effects)})"


