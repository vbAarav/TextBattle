import time

class ComplexEffect:
    def __init__(self, trigger, effect,
                 condition=None,
                 remove_effect=None,
                 max_duration=None, max_stack=None):
        
        self.trigger = trigger
        self.effect = effect
        self.condition = condition
        self.max_duration = max_duration
        self.max_stack = max_stack
        self.remove_effect = remove_effect
        
        self.is_active = False        
        self.current_duration = 0
        self.current_stack = 0
        
    def check_and_apply(self, passive, character, battle, **kwargs):
        if self.trigger and self.trigger(character, battle, **kwargs):
            if not(self.condition) or (self.condition and self.condition(character, battle, **kwargs)):
                if self.effect:
                    print(f"{character.name}'s {passive.name} has triggered")
                    time.sleep(1)
                    self.effect(character, battle, **kwargs)
                    self.is_active = True
                    self.current_stack += 1
                    
    def check_and_remove(self, passive, character, battle, **kwargs):
        if self.is_active and (self.max_duration and self.current_duration > self.max_duration):
            if self.remove_effect:
                print(f"{character.name}'s {passive.name} has deactivated")
                time.sleep(1)
                self.remove_effect(character, battle, **kwargs)
                self.is_active = False
                self.current_duration = 0
                
                
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

      
