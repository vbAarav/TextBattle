class Rune:
    def __init__(self, name, description=""):
        self.name = name
        self.description = description  # A brief description of the rune
    
    def __repr__(self):
        return f"Rune({self.name})"
    

class RuneSystem:
    def __init__(self):
        # Initialize the base runes and combinations        
        self.runes_combinations = {}
        self.runes = [
            Rune("Fire Rune"),
            Rune("Water Rune"),
            Rune("Grass Rune"),
            Rune("Earth Rune"),
            Rune("Air Rune"),
            Rune("Light Rune"),
            Rune("Dark Rune")
        ]
        self.add_combinations()
        
    def get_rune_by_name(self, name):
        runes = [rune for rune in self.runes if rune.name == name]
        if runes:
            return runes[0]
        return None

    def add_combinations(self):
        
        # Two Element Combinations
        self.add_combination_by_name("Fire Rune", "Water Rune", result_name="Steam Rune")
        self.add_combination_by_name("Fire Rune", "Grass Rune", result_name="Wildfire Rune")
        self.add_combination_by_name("Fire Rune", "Earth Rune", result_name="Lava Rune")
        self.add_combination_by_name("Fire Rune", "Air Rune", result_name="Ember Rune")
        self.add_combination_by_name("Fire Rune", "Light Rune", result_name="Flame Rune")
        self.add_combination_by_name("Fire Rune", "Dark Rune", result_name="Dark Fire Rune")
        
        self.add_combination_by_name("Water Rune", "Grass Rune", result_name="Swamp Rune")
        self.add_combination_by_name("Water Rune", "Earth Rune", result_name="Mud Rune")
        self.add_combination_by_name("Water Rune", "Air Rune", result_name="Mist Rune")
        self.add_combination_by_name("Water Rune", "Light Rune", result_name="Frost Rune")
        self.add_combination_by_name("Water Rune", "Dark Rune", result_name="Poison Rune")
        
        self.add_combination_by_name("Grass Rune", "Earth Rune", result_name="Forest Rune")
        self.add_combination_by_name("Grass Rune", "Air Rune", result_name="Breeze Rune")
        self.add_combination_by_name("Grass Rune", "Light Rune", result_name="Growth Rune")
        self.add_combination_by_name("Grass Rune", "Dark Rune", result_name="Decay Rune")
        
        self.add_combination_by_name("Earth Rune", "Air Rune", result_name="Dust Rune")
        self.add_combination_by_name("Earth Rune", "Light Rune", result_name="Radiance Rune")
        self.add_combination_by_name("Earth Rune", "Dark Rune", result_name="Oil Rune")
        
        self.add_combination_by_name("Air Rune", "Light Rune", result_name="Colour Rune")
        self.add_combination_by_name("Air Rune", "Dark Rune", result_name="Breeze Rune")
        
        self.add_combination_by_name("Light Rune", "Dark Rune", result_name="Order Rune")
        
        # Three Element Combinations
        self.add_combination_by_name("Fire Rune", "Water Rune", "Grass Rune", result_name="Nature Rune")
        self.add_combination_by_name("Fire Rune", "Water Rune", "Earth Rune", result_name="Volcanic Rune")
        self.add_combination_by_name("Fire Rune", "Water Rune", "Air Rune", result_name="Storm Rune")
        self.add_combination_by_name("Fire Rune", "Water Rune", "Light Rune", result_name="Rainbow Rune")
        self.add_combination_by_name("Fire Rune", "Water Rune", "Dark Rune", result_name="Rust Rune")
        
        # Four Element Combinations
        self.add_combination_by_name("Earth Rune", "Earth Rune", "Air Rune", "Water Rune", result_name="Ice Rune")
        
        # Seven Element Combinations
        self.add_combination_by_name("Fire Rune", "Fire Rune", "Fire Rune", "Fire Rune", "Fire Rune", "Fire Rune", "Fire Rune", result_name="Greater Fire Rune")
        self.add_combination_by_name("Water Rune", "Water Rune", "Water Rune", "Water Rune", "Water Rune", "Water Rune", "Water Rune", result_name="Greater Water Rune")
        self.add_combination_by_name("Grass Rune", "Grass Rune", "Grass Rune", "Grass Rune", "Grass Rune", "Grass Rune", "Grass Rune", result_name="Greater Grass Rune")
        self.add_combination_by_name("Earth Rune", "Earth Rune", "Earth Rune", "Earth Rune", "Earth Rune", "Earth Rune", "Earth Rune", result_name="Greater Earth Rune")
        self.add_combination_by_name("Air Rune", "Air Rune", "Air Rune", "Air Rune", "Air Rune", "Air Rune", "Air Rune", result_name="Greater Air Rune")
        self.add_combination_by_name("Light Rune", "Light Rune", "Light Rune", "Light Rune", "Light Rune", "Light Rune", "Light Rune", result_name="Greater Light Rune")
        self.add_combination_by_name("Dark Rune", "Dark Rune", "Dark Rune", "Dark Rune", "Dark Rune", "Dark Rune", "Dark Rune", result_name="Greater Dark Rune")        
        
    
    def add_combination_by_name(self, *rune_names, result_name):
        # Get all rune components
        runes = []
        for name in rune_names:
            rune = self.get_rune_by_name(name)
            if rune is None:
                rune = Rune(name)
                self.runes.append(rune)
            runes.append(rune)
            
        # Add the combination
        result = self.get_rune_by_name(result_name)
        if result is None:
            result = Rune(result_name)
            self.runes.append(result)
        self.runes_combinations[tuple(runes)] = result
            
    def get_combination_by_name(self, *rune_names):
        """Retrieve the combination result if it exists."""
        runes = [self.get_rune_by_name(name) for name in rune_names]
        result = self.runes_combinations.get(tuple(runes))
        if result:
            return result
        return None
    
    def display_combinations(self):
        """Display all the rune combinations."""
        for runes, result in self.runes_combinations.items():
            runes_names = " + ".join([rune.name for rune in runes])
            print(f"{runes_names} = {result}")
