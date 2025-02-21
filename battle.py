class Battle:
    def __init__(self, teamA, teamB):
        self.teamA = teamA
        self.teamB = teamB
        
    def start_battle(self):
        while any(c.is_alive() for c in self.teamA) and any(c.is_alive() for c in self.teamB):
            
            # Get all characters sorted by speed
            all_characters = sorted([c for c in self.teamA + self.teamB if c.is_alive()], key=lambda c: c.speed, reverse=True)
 
            for character in all_characters:
                if not character.is_alive():
                    continue
                
                # Get allies and enemies
                allies = self.teamA if character in self.teamA else self.teamB
                enemies = self.teamB if character in self.teamA else self.teamA
                
                self.choose_action(character, allies, enemies)

        # End of battle
        if any(c.is_alive() for c in self.teamA):
            print("Team 1 wins!")
        else:
            print("Team 2 wins!")

    # Choose an Action
    def choose_action(self, character, allies, enemies):
        print(f"\n{character.name}'s turn!")
        print("1. Attack")
        print("2. Magic (not implemented yet)")
        
        choice = input("Choose an action: ").strip()
        if choice == "1":
            self.attack_action(character, allies, enemies)          
        
        elif choice == "2":
            print(f"{character.name} tries to cast magic, but it's not implemented yet!")
            
        else:
            print("Invalid action!")
            
    # All Action Types 
    def attack_action(self, character, allies, enemies):
        target = self.choose_target(allies + enemies)
        if target:
            character.attack_target(target)
        
    # Choose a Target
    def choose_target(self, targets, condition=True):       
        print("\nChoose a target:")
        targets = [t for t in targets if condition]
        for i, target in enumerate(targets):
            print(f"{i+1}. {target.name} (HP: {target.hp})")
        
        choice = input("Enter target number: ").strip()
        if choice.isdigit():
            index = int(choice) - 1
            if 0 <= index < len(targets):
                return targets[index]
        print("Invalid choice!")
        return None