import random
import battle
import players

class Area:
    # Constructor
    def __init__(self, name, description=None, nbrs=None):
        self.name = name
        self.description = description
        self.nbrs = nbrs if nbrs is not None else []
        self.enemies = {}
        
    # Events
    def explore_area(self, player):
        enemies = random.choices(list(self.enemies.keys()), weights=self.enemies.values(), k=1)
        battle.Battle(player, players.Enemy(characters=enemies)).start_battle()
    
    # Getters and Setters
    def add_neighbour(self, area):
        self.nbrs.append(area)
        
    def add_enemy(self, enemy, spawn_weight):
        self.enemies[enemy] = spawn_weight

    # Magic Functions
    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name
    
class Map:
    def __init__(self, areas=None):
        self.areas = [] if areas is None else areas
        
    def add_area(self, area):
        if area:
            self.areas.append(area)
        
    def get_area_by_name(self, name):
        for area in self.areas:
            if area.name == name:
                return area
        return None
                
    def find_new_location(self, player, start):
        print("\nWhere would you like to go?")
        print(f"1. {start}")
        for i, area in enumerate(start.nbrs):
            print(f"{i+2}. {area}")
        
        choice = player.get_input("Choose a location: ", [str(i+1) for i in range(len(start.nbrs) + 1)])
        if choice.isdigit():
            index = int(choice) - 1
            if 0 <= index and index <= len(start.nbrs):
                return start if index == 0 else start.nbrs[index]
        print("Invalid choice!")
        
        
    