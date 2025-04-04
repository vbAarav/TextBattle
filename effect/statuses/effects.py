from magic.sigils import Sigil
from effect.effects import ComplexEffect
from character.characters import Damage
from effect.statuses.status_effect import StatusEffect
import effect.effects as effects
import math

# Poison
def poison(character, battle, **kwargs):
    damage_amount = int(math.floor(character.max_hp.total * 0.06))
    print(f"{character.name} is poisoned")
    character.take_damage(damage_amount, battle)

POISON = StatusEffect("Poison", description="Takes 6% of Max HP as damage at the start of turn", effects=[ComplexEffect(effects.trigger_on_start_of_turn, poison)])

# Stun
def stun(character, battle, **kwargs):
    print(f"{character.name} is stunned")

STUN = StatusEffect("Stun", description="Target cannot act when under this effect", effects=[ComplexEffect(effects.trigger_on_start_of_character_turn, stun)])