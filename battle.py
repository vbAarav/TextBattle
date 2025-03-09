import time
import effects

class Battle:
    # Constructor
    def __init__(self, playerOne, playerTwo):
        self.playerOne = playerOne
        self.playerTwo = playerTwo
        self.turn = 0
        
    def __repr__(self):
        toReturn = "\n-----------------------------------------"
        toReturn += f"\n                 Turn: {self.turn}"
        toReturn += f"\n{self.playerOne.name}:"
        for character in self.playerOne.characters:
            toReturn += f"\n{character}"
        toReturn += "\n-----------------------------------------"
        toReturn += f"\n{self.playerTwo.name}:"
        for character in self.playerTwo.characters:
            toReturn += f"\n{character}"
        toReturn += "\n-----------------------------------------"
        return toReturn

    # Get Methods
    def get_all_characters(self):
        return self.playerOne.characters + self.playerTwo.characters
    def get_character_allies(self, character):
        if character in self.playerOne.characters:
            return self.playerOne.characters
        return self.playerTwo.characters

    def get_character_enemies(self, character):
        if character in self.playerOne.characters:
            return self.playerTwo.characters
        return self.playerOne.characters
    
    def get_player(self, character):
        if character in self.playerOne.characters:
            return self.playerOne
        return self.playerTwo
    
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
        print(self)
        time.sleep(1)

    # Start the Battle
    def start_battle(self):
        # Start of Battles
        self.turn = 0
        
        # Trigger Start of Battle Effects
        for character in self.get_all_characters():
                self.trigger_effects(character, trigger="on_start_of_battle")              

        # Battle Loop
        while any(c.is_alive() for c in self.playerOne.characters) and any(c.is_alive() for c in self.playerTwo.characters):   

            # Calculate Turn Order
            all_characters = sorted([c for c in self.get_all_characters() if c.is_alive()], key=lambda c: c.speed.total, reverse=True)

            # Character Turns
            for character in all_characters:
                if not character.is_alive():
                    continue
                
                # Start of Turn
                self.turn += 1
                
                # Trigger Start of Turn Effects
                for chr in self.get_all_characters():
                    self.trigger_effects(chr, trigger="on_start_of_turn", turn=self.turn)
                
                time.sleep(1)
                self.display_battle_status() # Display Battle Status
                self.choose_action(character)  # Choose Action
                
        self.end_battle()

        
            
    def end_battle(self):   
        # End of battle
        if any(c.is_alive() for c in self.playerOne.characters):
            print(f"{self.playerOne} wins!")
        else:
            print(f"{self.playerTwo} wins!")
        

    # Choose an Action
    def choose_action(self, character):
        print(f"\n{character.name}'s turn!")
        print("1. Attack")
        print("2. Rune" if len([effect for runes in character.runes for effect in runes.active_effects]) > 0 else "")

        # Choose Action
        choices = ["1"]
        choices.append("2") if len([effect for runes in character.runes for effect in runes.active_effects]) > 0 else None
        choice = self.get_player(character).get_input("Choose an action: ", choices)
        valid_choice = False
        
        # Execute Chosen Action
        while not valid_choice:
            if choice == "1":
                valid_choice = self.attack_action(character)

            elif choice == "2" and len([effect for runes in character.runes for effect in runes.active_effects]) > 0:
                valid_choice = self.use_rune_action(character)

            else:
                print("Invalid action!")
            
    
    # All Action Types
    def attack_action(self, character):
        target = self.choose_target(self.get_all_characters(), character)
        if target:
            character.attack_target(target, self)
            return True
        else:
            return False

    def use_rune_action(self, character):
        rune = self.choose_rune(character)
        if rune:
            active_effect = self.choose_active_effect(rune)
            if active_effect:
                character.activate_active_effect(rune, active_effect, self)
                return True
            else:
                return False
        else:
            return False

    # Choose a Selection
    def choose_target(self, targets, character, condition=True):
        print("\nChoose a target:")
        time.sleep(1)
        
        # Display Targets
        targets = [t for t in targets if condition]
        for i, target in enumerate(targets):
            print(f"{i+1}. {target}")
            
        time.sleep(1)
        choice = self.get_player(character).get_input("Enter target number: ", [str(i+1) for i in range(len(targets))])
        if choice.isdigit():
            index = int(choice) - 1
            if 0 <= index < len(targets):
                return targets[index]
        print("Invalid choice!")
        return None

    def choose_rune(self, character):
        if character.runes:
            print("\nChoose a rune:")
            time.sleep(1)
            
            for i, rune in enumerate(character.runes):
                print(f"{i+1}. {rune.name}: {rune.description}")

            time.sleep(1)
            choice = self.get_player(character).get_input("Enter rune number: ", [str(i+1) for i in range(len(character.runes))])
            if choice.isdigit():
                index = int(choice) - 1
                if 0 <= index < len(character.runes):
                    return character.runes[index]
            print("Invalid choice!")
            return None
        return None

    def choose_active_effect(self, rune):
        if rune.active_effects:
            print("\nChoose an active effect:")
            time.sleep(1)
            for i, effect in enumerate(rune.active_effects):
                print(f"{i+1}. {effect.name}: {effect.description}")

            time.sleep(1)
            choice = self.get_player(rune.equipped_character).get_input("Enter effect number: ", [str(i+1) for i in range(len(rune.active_effects))])
            if choice.isdigit():
                index = int(choice) - 1
                if 0 <= index < len(rune.active_effects):
                    return rune.active_effects[index]
            print("Invalid choice!")
            return None
        return None
