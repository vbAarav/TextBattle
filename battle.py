import time
import math

class Battle:
    # Constructor
    def __init__(self, playerOne, playerTwo):
        self.playerOne = playerOne
        self.playerTwo = playerTwo
        self.turn = 0
        self.character_turns = {}
        self.winner = None

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

    def get_winner(self):
        if self.winner:
            return self.winner

    # Battle Methods
    def display_battle_status(self):
        print(self)
        time.sleep(1)
        
    def can_battle_continue(self):
        return any(c.is_alive() for c in self.playerOne.characters) and any(c.is_alive() for c in self.playerTwo.characters)
        
    def trigger_effects(self, character, trigger, **kwargs):
        # Status Effects
        for effect in character.status_effects:
            effect.check(character, self, **kwargs, trigger=trigger)

        # Sigil Effects
        for sigil in character.sigils:
            for effect in sigil.passive_effects:
                effect.check(character, self, **kwargs, trigger=trigger)

    def add_duration_all(self):
        for character in self.get_all_characters():
            self.add_duration(character)
                
    def add_duration(self, character):
        # Status Effects
        for effect in character.status_effects:
            effect.add_duration(character, self)
        
        # Sigil Effects
        for sigil in character.sigils:
            for passive in sigil.passive_effects:
                passive.add_duration(self)
                
    def next_turn(self, character):
        # Check if character can act
        if character.can_act():
            self.turn += 1 
            self.character_turns[character] += 1
            self.add_duration(character)
            self.trigger_effects(character, trigger="on_start_of_turn_x", turn=self.turn)
            self.trigger_effects(character, trigger="on_start_of_character_turn", turn=self.turn)
            for chr in self.get_all_characters():
                self.trigger_effects(chr, trigger="on_start_of_turn", turn=self.turn)   
            time.sleep(1) 
            
            self.display_battle_status()  # Display Battle Status
            self.choose_action(character)  # Choose Action
        else:
            print(f"{character.name} is unable to ACT")
            self.add_duration(character)

    # Start the Battle
    def start_battle(self):
        self.turn = 0
        self.character_turns = {chr : 0 for chr in self.get_all_characters()}
        AP_THRESHOLD = sum([c.speed.total for c in self.get_all_characters()]) * 2

        # Trigger Start of Battle Effects
        for character in self.get_all_characters():
            self.trigger_effects(character, trigger="on_start_of_battle")

        # Battle Loop
        while self.can_battle_continue():
            # Increase Action Points
            for character in self.get_all_characters():
                character.action_points.base_value += (((50 * math.sqrt(character.speed.total / 50)) * 100)/(AP_THRESHOLD))
            
            # Determine Next Characters
            active_characters = [c for c in self.get_all_characters() if c.action_points.total >= AP_THRESHOLD]
            active_characters.sort(key=lambda c: c.speed.total, reverse=True)
            
            # Determine Speed Ties
            for character in active_characters:
                if not self.can_battle_continue():
                    break
                if not character.is_alive():
                    continue
                
                self.next_turn(character)
                character.action_points.clear_modifiers()
                character.action_points.base_value = 0

        self.end_battle()

    def end_battle(self):
        # End of battle
        for character in self.get_all_characters():
            character.clear_stat_modifiers()
        if any(c.is_alive() for c in self.playerOne.characters):
            print(f"{self.playerOne} wins!")
            self.winner = self.playerOne
        else:
            print(f"{self.playerTwo} wins!")
            self.winner = self.playerTwo

    # Choose an Action
    def choose_action(self, character):
        print(f"\n{character.name}'s turn!")
        print("1. Attack")
        print("2. Sigil" if len([effect for sigils in character.sigils for effect in sigils.active_effects]) > 0 else "")

        # Choose Action
        choices = ["1"]
        choices.append("2") if len([effect for sigils in character.sigils for effect in sigils.active_effects]) > 0 else None
        choice = self.get_player(character).get_input("Choose an action: ", choices)
        valid_choice = False

        # Execute Chosen Action
        while not valid_choice:
            if choice == "1":
                valid_choice = self.attack_action(character)

            elif choice == "2" and len([effect for sigils in character.sigils for effect in sigils.active_effects]) > 0:
                valid_choice = self.use_sigil_action(character)

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

    def use_sigil_action(self, character):
        sigil = self.choose_sigil(character)
        if sigil:
            active_effect = self.choose_active_effect(sigil)
            if active_effect:
                character.activate_active_effect(sigil, active_effect, self)
                return True
            else:
                return False
        else:
            return False

    # Choose a Selection
    def choose_target(self, targets, character):
        print("\nChoose a target:")
        time.sleep(1)

        choices = []
        # Display Ally Targets
        allies = [c for c in targets if c in self.get_character_allies(character)]
        print(f"-------Allies-------")
        for i, target in enumerate(allies):
            print(f"{i+1}. {target}")
            choices.append(str(i+1))

        # Display Enemy Targets
        enemies = [c for c in targets if c in self.get_character_enemies(character)]
        print(f"\n-------Enemies-------")
        for i, target in enumerate(enemies):
            print(f"{i+1+len(allies)}. {target}")
            choices.append(str(i+1+len(allies)))

        time.sleep(1)
        choice = self.get_player(character).get_input("Enter target number: ", choices)
        if choice.isdigit():
            index = int(choice) - 1
            if 0 <= index < len(targets):
                return targets[index]
        print("Invalid choice!")
        return None

    def choose_sigil(self, character):
        if character.sigils:
            print("\nChoose a sigil:")
            time.sleep(1)

            for i, sigil in enumerate(character.sigils):
                print(f"{i+1}. {sigil.name}: {sigil.description}")

            time.sleep(1)
            choice = self.get_player(character).get_input("Enter sigil number: ", [
                str(i+1) for i in range(len(character.sigils))])
            if choice.isdigit():
                index = int(choice) - 1
                if 0 <= index < len(character.sigils):
                    return character.sigils[index]
            print("Invalid choice!")
            return None
        return None

    def choose_active_effect(self, sigil):
        if sigil.active_effects:
            print("\nChoose an active effect:")
            time.sleep(1)
            for i, effect in enumerate(sigil.active_effects):
                print(f"{i+1}. {effect.name}: {effect.description}")

            time.sleep(1)
            choice = self.get_player(sigil.equipped_character).get_input(
                "Enter effect number: ", [str(i+1) for i in range(len(sigil.active_effects))])
            if choice.isdigit():
                index = int(choice) - 1
                if 0 <= index < len(sigil.active_effects):
                    return sigil.active_effects[index]
            print("Invalid choice!")
            return None
        return None
