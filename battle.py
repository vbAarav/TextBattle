import time

class Battle:
    # Constructor
    def __init__(self, teamA, teamB):
        self.teamA = teamA
        self.teamB = teamB
        self.turn = 0

    # Get Methods
    def get_character_allies(self, character):
        if character in self.teamA:
            return self.teamA
        return self.teamB

    def get_character_enemies(self, character):
        if character in self.teamA:
            return self.teamB
        return self.teamA
    
    # Battle Methods
    def trigger_effects(self, character, trigger, **kwargs):
        # Status Effects
        for effect in character.status_effects:
            effect.update_effect(character, self, **kwargs, trigger=trigger)
        
        # Rune Effects
        for rune in character.runes:
            for effect in rune.passive_effects:
                effect.check_and_apply(character, self, **kwargs, trigger=trigger)
    
    def display_battle_status(self):
        print("\n-----------------------------------------")
        print(f"Turn: {self.turn}")
        print("Team 1:")
        for character in self.teamA:
            print(f"{character.name} (HP: {character.hp}/{character.max_hp}) (ATK: {character.attack}) (DEF: {character.defense}) (SPD: {character.speed})")
        print("Team 2:")
        for character in self.teamB:
            print(f"{character.name} (HP: {character.hp}/{character.max_hp}) (ATK: {character.attack}) (DEF: {character.defense}) (SPD: {character.speed})")
        print("\n-----------------------------------------")
        time.sleep(1)

    # Start the Battle
    def start_battle(self):
        # Start of Battle
        self.turn = 0

        # Trigger Start of Battle Effects
        for team in [self.teamA, self.teamB]:
            for character in team:
                self.trigger_effects(character, trigger="on_start_of_battle")              

        # Battle Loop
        while any(c.is_alive() for c in self.teamA) and any(c.is_alive() for c in self.teamB):   

            # Calculate Turn Order
            all_characters = sorted([c for c in self.teamA + self.teamB if c.is_alive()], key=lambda c: c.speed, reverse=True)

            # Character Turns
            for character in all_characters:
                if not character.is_alive():
                    continue
                
                # Start of Turn
                self.turn += 1
                
                # Trigger Start of Turn Effects
                for team in [self.teamA, self.teamB]:
                    for chr in team:
                        self.trigger_effects(chr, trigger="on_start_of_turn", turn=self.turn)
                
                time.sleep(1)
                self.display_battle_status() # Display Battle Status
                self.choose_action(character)  # Choose Action

        # End of battle
        if any(c.is_alive() for c in self.teamA):
            print("Team 1 wins!")
        else:
            print("Team 2 wins!")

    # Choose an Action
    def choose_action(self, character):
        print(f"\n{character.name}'s turn!")
        print("1. Attack")
        print("2. Rune")

        choice = self.get_input("Choose an action: ", ["1", "2"])
        if choice == "1":
            self.attack_action(character)

        elif choice == "2":
            self.use_rune_action(character)

        else:
            print("Invalid action!")
            
    def get_input(self, message, valid_choices):
        choice = input(message).strip()
        while choice not in valid_choices:
            print("Invalid input!")
            time.sleep(1)
            choice = input(message).strip()
        return choice
    
    # All Action Types
    def attack_action(self, character):
        target = self.choose_target(self.teamA + self.teamB)
        if target:
            character.attack_target(target, self)

    def use_rune_action(self, character):
        rune = self.choose_rune(character)
        if rune:
            active_effect = self.choose_active_effect(rune)
            if active_effect:
                character.activate_active_effect(rune, active_effect, self)

    # Choose a Selection
    def choose_target(self, targets, condition=True):
        print("\nChoose a target:")
        time.sleep(1)
        
        targets = [t for t in targets if condition]
        for i, target in enumerate(targets):
            print(f"{i+1}. {target.name} (HP: {target.hp}/{target.max_hp}) (ATK: {target.attack}) (DEF: {target.defense}) (SPD: {target.speed})")
            
        time.sleep(1)
        choice = self.get_input("Enter target number: ", [str(i+1) for i in range(len(targets))])
        if choice.isdigit():
            index = int(choice) - 1
            if 0 <= index < len(targets):
                return targets[index]
        print("Invalid choice!")
        return None

    def choose_rune(self, character):
        print("\nChoose a rune:")
        time.sleep(1)
        
        for i, rune in enumerate(character.runes):
            print(f"{i+1}. {rune.name}: {rune.description}")

        time.sleep(1)
        choice = self.get_input("Enter rune number: ", [str(i+1) for i in range(len(character.runes))])
        if choice.isdigit():
            index = int(choice) - 1
            if 0 <= index < len(character.runes):
                return character.runes[index]
        print("Invalid choice!")
        return None

    def choose_active_effect(self, rune):
        print("\nChoose an active effect:")
        time.sleep(1)
        for i, effect in enumerate(rune.active_effects):
            print(f"{i+1}. {effect.name}: {effect.description}")

        time.sleep(1)
        choice = self.get_input("Enter effect number: ", [str(i+1) for i in range(len(rune.active_effects))])
        if choice.isdigit():
            index = int(choice) - 1
            if 0 <= index < len(rune.active_effects):
                return rune.active_effects[index]
        print("Invalid choice!")
        return None
