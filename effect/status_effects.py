from magic.sigils import Sigil
from effect.effect_base import ComplexEffect, StatusEffect, StatusType
from character.characters import Damage
import effect.effect_base as effect_base
import math

# Poison
POISON = StatusEffect(
    "Poison",
     description="Target takes 6% of Max HP as Damage at the start of turn",
     type=StatusType.DEBUFF,
     effects=
     [
        ComplexEffect(effect_base.trigger_on_start_of_turn, lambda character, battle, **kwargs: poison(character, battle, **kwargs))
     ]
)
def poison(character, battle, **kwargs):
    damage_amount = int(math.floor(character.max_hp.total * 0.06))
    print(f"{character.name} is poisoned")
    character.take_damage(damage_amount, battle)

# Stun
STUN = StatusEffect(
    "Stun",
     description="Target cannot act when under this effect",
     type=StatusType.DEBUFF,
     on_apply=lambda character, battle, **kwargs: apply_stun(character, battle, **kwargs),
     remove_effect=lambda character, battle, **kwargs: remove_stun(character, battle, **kwargs),
     effects=[]
)
def apply_stun(character, battle, **kwargs):
    character.acts = False

def remove_stun(character, battle, **kwargs):
    character.acts = True
