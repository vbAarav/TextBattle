import time
from effect.effects import ComplexEffect               
                
class PassiveEffect:
    def __init__(self, name, effects: list[ComplexEffect], description=""):
        self.name = name
        self.description = description        
        self.effects = effects
        
    def check(self, character, battle, **kwargs):
        for complex_effect in self.effects:
            if not(complex_effect.max_stack) or (complex_effect.current_stack < complex_effect.max_stack):
                complex_effect.check_and_apply(self, character, battle, **kwargs)
            if complex_effect.is_active:
                complex_effect.check_and_remove(self, character, battle, **kwargs)
                
    def add_duration(self, battle):
        for complex_effect in self.effects:
            if complex_effect.is_active:
                complex_effect.current_duration += 1

    def __repr__(self):
        return f"PassiveEffect({self.name})" 

      
