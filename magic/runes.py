class Rune:
    def __init__(self, name):
        self.name = name
    
    def __repr__(self):
        return f"R-{self.name}";

FIRE = Rune("Fire")
WATER = Rune("Water")
EARTH = Rune("Earth")
WIND = Rune("Wind")
DARK = Rune("Dark")
LIGHT = Rune("Light")
ICE = Rune("Ice")
GRASS = Rune("Grass")
SPACE = Rune("Space")