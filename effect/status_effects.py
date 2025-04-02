from magic.sigils import Sigil
from effect.effects import StatusEffect
import effect.effects as effects

# Status Effects
def poison(character, battle):
    damage = character.max_hp.total * 0.06
    print(f"{character.name} is poisoned")
    character.take_damage(damage, battle)


POISON = StatusEffect("Poison", description="Takes 6% of Max HP as damage at the start of turn",
                                    duration=3, ongoing_effect=poison, trigger_condition=effects.trigger_on_start_of_turn)


def stun(character, battle):
    print(f"{character.name} is stunned")

STUN = StatusEffect("Stun", description="Skips the character's turn", duration=1,
                                  ongoing_effect=stun, trigger_condition=effects.trigger_on_start_of_character_turn)