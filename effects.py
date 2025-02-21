# Base Effect Class
class Effect:
    def __init__(self, name, description=""):
        self.name = name
        self.description = description

    def apply(self, character, battle):
        # General method to apply an effect
        raise NotImplementedError("Subclasses must implement the 'apply' method.")
        
    def __repr__(self):
        return f"Effect({self.name})"


class ActiveEffect(Effect):
    def __init__(self, name, description="", effect_function=None):
        super().__init__(name, description)
        self.effect_function = effect_function  # Function to apply the active effect

    def apply(self, character, battle):
        if self.effect_function:
            self.effect_function(character, battle)
        
    def __repr__(self):
        return f"ActiveEffect({self.name})"


class PassiveEffect(Effect):
    def __init__(self, name, description="", effect_function=None):
        super().__init__(name, description)
        self.effect_function = effect_function  # Function to apply the passive effect
    
    def apply(self, character, battle):
        # Passive effects may be triggered on certain events automatically
        if self.effect_function:
            self.effect_function(character, battle)
        
    def __repr__(self):
        return f"PassiveEffect({self.name})"
    
# Active Effects
def large_slice(character, battle):
    target = battle.choose_target(battle.teamA + battle.teamB)
    if target:
        print(f"{character.name} attacks {target.name}!")
        damage = int(character.attack * 1.5)
        target.receive_attack(damage)

def heal_all_allies(character, battle):
    for ally in battle.get_character_allies(character):
        heal_amount = ally.max_hp * 0.5
        ally.receive_heal(heal_amount)

def swap_atk_def(character, battle):
    character.attack, character.defense = character.defense, character.attack
    print(f"{character.name} swapped ATK and DEF stats.")

def damage_ally_and_poison_enemy(character, battle):
    target = battle.choose_target(battle.teamA + battle.teamB)
    if (target in battle.get_character_allies(character)) and (target != character):
        # Deal Damage
        print(f"{character.name} attacks {target.name}!")
        damage = int(character.attack * 1.2)
        target.receive_attack(damage)
        
        # Poison
        
    else:
        # Deal Damage
        print(f"{character.name} attacks {target.name}!")
        damage = int(character.attack * 0.5)
        target.receive_attack(damage)


# Passive Effects
def thousand_divine_cuts(character, battle):
    print("Effect Running")

def extra_damage_on_no_damage(character, battle):
    print("Effect Running")
        
        
        
# Create A Large Set of Effects
effect_large_slice = ActiveEffect("Large Slice", description="Deals damage to the target equal to (150%) of ATK", effect_function=large_slice)
effect_heal_all = ActiveEffect("Heal All", description="All allies heal health equal to (50%) of MAXHP", effect_function=heal_all_allies)
effect_guard_switch = ActiveEffect("Guard Switch", description="Swaps the character's ATK and DEF stats", effect_function=swap_atk_def)
effect_enforced_vigor = ActiveEffect("Enforced Vigor", description="Deals damage to the target equal to (50%) of ATK. (120%) of ATK if the target is an ally", effect_function=damage_ally_and_poison_enemy)

effect_thousand_divine_cuts = PassiveEffect("Thousand Divine Cuts", description="All enemies have DEF reduced by (5%)", effect_function=thousand_divine_cuts)
