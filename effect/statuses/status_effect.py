import time
from effect.effects import ComplexEffect 
from enum import Enum, auto 
from character.characters import Stat

class StatusType(Enum):
    BUFF = auto()
    DEBUFF = auto()
    NEUTRAL = auto()

class StatusEffect:
    def __init__(self, name, effects: list[ComplexEffect], type=StatusType.NEUTRAL, description="",
                 condition=None, remove_effect=None,
                 max_duration=None, max_stack=None):
        self.name = name
        self.description = description        
        self.effects = effects
        self.type = type;
        
        self.condition = condition
        self.max_duration = max_duration
        self.max_stack = max_stack
        self.remove_effect = remove_effect
        
        self.is_active = False        
        self.current_duration = 0
        self.current_stack = 0
        
    def check(self, character, battle, **kwargs):
        for complex_effect in self.effects:
            if not(complex_effect.max_stack) or (complex_effect.current_stack < complex_effect.max_stack):
                complex_effect.check_and_apply(self, character, battle, **kwargs)
            if complex_effect.is_active:
                complex_effect.check_and_remove(self, character, battle, **kwargs)
    
    def check_and_remove(self, passive, character, battle, **kwargs):
        if self.is_active and (self.max_duration and self.current_duration > self.max_duration):
            if self.remove_effect:
                print(f"{character.name}'s {passive.name} has deactivated")
                time.sleep(1)
                self.remove_effect(character, battle, **kwargs)
                self.is_active = False
                self.current_duration = 0
    
    def remove(self, character, battle):
        print(f"{character.name}'s {self.name} has been removed")
        time.sleep(1)
        character.status_effects.remove(self)
                
    def add_duration(self, character, battle):
        self.current_duration += 1
        if self.max_duration and self.current_duration >= self.max_duration:
            self.remove(character, battle)
            
        for complex_effect in self.effects:
            if complex_effect.is_active:
                complex_effect.current_duration += 1
                
    def get_duration(self):
        if self.max_duration:
            return self.max_duration - self.current_duration
        else:
            return self.current_duration

    def __repr__(self):
        return f"{self.name}: |{self.get_duration()}|{self.current_stack}|" 
    

    
