import effects

class Rune:
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
        return f"Rune({self.name}, ActiveEffects: {len(self.active_effects)}, PassiveEffects: {len(self.passive_effects)})"


# Test Runes
power_rune = Rune(
    name="Power Rune",
    active_effects=[effects.effect_large_slice, effects.effect_enforced_vigor],
    passive_effects=[effects.effect_thousand_divine_cuts, effects.effect_early_stance, effects.effect_double_up, effects.effect_engine, effects.effect_late_bloomer, effects.effect_last_stance, effects.effect_wolf_hunger]
)

crystalised_ice_rune = Rune(
    name="Crystalised Ice Rune",
    active_effects=[effects.effect_guard_switch]
)

glowing_grass_rune = Rune(
    name="Glowing Grass Rune",
    active_effects=[effects.effect_heal_all]
)