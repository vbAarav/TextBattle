class Character:
    def __init__(self, name, hp, attack, defense, speed, runes=[]):
        # Stats
        self.name = name
        self.hp = hp
        self.attack = attack
        self.speed = speed
        self.defense = defense
        
        # Runes
        self.runes = runes
        
    def equip_rune(self, rune):
        self.runes.append(rune)
        
    # Is the Character Alive
    def is_alive(self):
        return self.hp > 0

    # Attack Methods
    def receive_attack(self, damage):
        self.hp = max(0, self.hp - (damage - self.defense))
        print(f"{self.name} takes {damage} damage! HP: {self.hp}")

    def attack_target(self, target):
        print(f"{self.name} attacks {target.name}!")
        target.receive_attack(self.attack)

    
    

    