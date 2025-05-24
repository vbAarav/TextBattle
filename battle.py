# battle.py
import math

class Battle:
    """
    A battle between two Player objects (playerOne vs. playerTwo).
    Each has a list of characters, each character has stats, sigils, etc.
    """

    def __init__(self, playerOne, playerTwo, gui_request):
        """
        gui_request: a function with signature
            gui_request(request_type, **kwargs)
        that the Battle object will call whenever it wants to:
          - display_battle_status
          - choose_action
          - choose_target
          - choose_sigil
          - choose_active_effect
          - display_winner
        """
        self.playerOne = playerOne
        self.playerTwo = playerTwo
        self.turn = 0
        self.character_turns = {}
        self.winner = None

        # gui_request is a callback we call instead of printing/asking console
        self.gui_request = gui_request

    def __repr__(self):
        """
        Return a string snapshot of current battle state:
        turn number, each player's characters, their HP, etc.
        """
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

    # ---------------------------------------------------
    #  ACCESSORS
    # ---------------------------------------------------
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
        return self.winner

    # ---------------------------------------------------
    #  DISPLAY / PAUSE METHODS (GUI‐driven)
    # ---------------------------------------------------
    def _display_battle_status(self):
        """
        Instead of print(...), call the GUI callback.
        """
        status_text = repr(self)
        # Let the GUI know it should redraw the status on screen
        self.gui_request("display_battle_status", status=status_text)

    def _pause(self, seconds=1):
        """
        If you want a small pause between turns/effects,
        tell the GUI to wait that many seconds.
        """
        self.gui_request("pause", duration=seconds)

    # ---------------------------------------------------
    #  BATTLE “CORE” LOOP
    # ---------------------------------------------------
    def can_battle_continue(self):
        """Return True if both sides have at least one character alive."""
        return (
            any(c.is_alive() for c in self.playerOne.characters)
            and any(c.is_alive() for c in self.playerTwo.characters)
        )

    def trigger_effects(self, character, trigger, **kwargs):
        """
        Run all status/sigil effects that respond to a given trigger.
        """
        # Status Effects
        for effect in character.status_effects:
            effect.check(character, self, **kwargs, trigger=trigger)

        # Sigil Effects
        for sigil in character.sigils:
            for effect in sigil.passive_effects:
                effect.check(character, self, **kwargs, trigger=trigger)

    def add_duration(self, character):
        """
        Increment duration of all status/sigil effects for this character.
        """
        for effect in character.status_effects:
            effect.add_duration(character, self)
        for sigil in character.sigils:
            for passive in sigil.passive_effects:
                passive.add_duration(self)

    def add_duration_all(self):
        """Do add_duration(...) for every character in the battle."""
        for character in self.get_all_characters():
            self.add_duration(character)

    def next_turn(self, character):
        """
        Called when it’s `character`’s turn to act.
        If they can act, we increment turn, apply “on_start” effects,
        display status, and then call choose_action(character).
        """
        if character.can_act():
            self.turn += 1
            self.character_turns[character] += 1

            self.add_duration(character)
            self.trigger_effects(character, trigger="on_start_of_turn_x", turn=self.turn)
            self.trigger_effects(character, trigger="on_start_of_character_turn", turn=self.turn)
            for chr_ in self.get_all_characters():
                self.trigger_effects(chr_, trigger="on_start_of_turn", turn=self.turn)

            # Display updated battle status via GUI
            self._display_battle_status()
            # Optionally, pause 0.5s so user can read it
            self._pause(0.5)

            # Now let the user choose an action
            self._choose_action(character)

        else:
            # Character cannot act: still add durations, display a short message
            self.add_duration(character)
            self.gui_request("display_temporary_message", text=f"{character.name} is unable to act!")
            self._pause(0.5)

    # ---------------------------------------------------
    #  START & END
    # ---------------------------------------------------
    def start_battle(self):
        """
        The main battle loop (replacing print/input with GUI callbacks).
        """

        # 1) Initialize turn counts and trigger “on_start_of_battle”
        self.turn = 0
        self.character_turns = {c: 0 for c in self.get_all_characters()}

        for character in self.get_all_characters():
            self.trigger_effects(character, trigger="on_start_of_battle")

        # 2) Main loop
        while self.can_battle_continue():
            # Increase Action Points
            AP_THRESHOLD = sum(c.speed.total for c in self.get_all_characters()) * 2
            for character in self.get_all_characters():
                # formula: ((50 * sqrt(speed/50))*100)/AP_THRESHOLD
                gain = ((50 * math.sqrt(character.speed.total / 50)) * 100) / AP_THRESHOLD
                character.action_points.base_value += gain

            # Determine who ready to act
            active_characters = [
                c for c in self.get_all_characters() if c.action_points.total >= AP_THRESHOLD
            ]
            active_characters.sort(key=lambda c: c.speed.total, reverse=True)

            for character in active_characters:
                if not self.can_battle_continue():
                    break
                if not character.is_alive():
                    continue

                # It’s `character`’s turn
                self.next_turn(character)
                # Clear AP modifiers & reset AP to zero
                character.action_points.clear_modifiers()
                character.action_points.base_value = 0

        # 3) Once loop ends, determine winner
        self._end_battle()

    def _end_battle(self):
        """
        Called after the while‐loop in start_battle ends.
        """
        # Clear all stat modifiers
        for character in self.get_all_characters():
            character.clear_stat_modifiers()

        # Decide winner
        if any(c.is_alive() for c in self.playerOne.characters):
            winner = self.playerOne
        else:
            winner = self.playerTwo

        self.winner = winner
        self.gui_request("display_winner", winner=winner)

    # ---------------------------------------------------
    #  CHOICE ROUTINES (GUI‐driven)
    # ---------------------------------------------------
    def _choose_action(self, character):
        """
        Instead of printing “1. Attack / 2. Sigil”, we call the GUI:
        """
        # First see if character has any active sigils:
        has_active_sigil = any(
            len(sigil.active_effects) > 0 for sigil in character.sigils
        )
        self.gui_request(
            "choose_action",
            character=character,
            can_use_sigil=has_active_sigil,
        )
        # Now the GUI must wait for either “attack_chosen” or “sigil_chosen” event,
        # which it will send back by calling battle.action_chosen_callback(…).

    def attack_action(self, character):
        """
        Called once the GUI has told us “attack” was clicked.
        We now need to let the user pick a target.
        """
        all_chars = self.get_all_characters()
        self.gui_request("choose_target", character=character, targets=all_chars)

        # Now the GUI needs to call back attack_chosen_target(character, chosen_target)
        # to finalize the attack.

    def use_sigil_action(self, character):
        """
        Called once the GUI has told us “use sigil” was clicked.
        """
        if not character.sigils:
            # shouldn’t happen: GUI wouldn’t let us pick “use sigil” if none exist
            self.gui_request("display_temporary_message", text="No sigils available!")
            return

        self.gui_request("choose_sigil", character=character, sigils=character.sigils)
        # GUI will call back use_sigil_chosen(character, chosen_sigil)

    def choose_active_effect(self, sigil):
        """
        GUI already called “choose_sigil” and got back a sigil; now pick which effect:
        """
        if not sigil.active_effects:
            self.gui_request("display_temporary_message", text="No active effects!")
            return

        self.gui_request(
            "choose_active_effect", 
            sigil=sigil, 
            active_effects=sigil.active_effects
        )
        # GUI will call back use_active_effect_chosen(sigil, chosen_effect)

    # ---------------------------------------------------
    #  CALLBACKS THAT GUI WILL INVOKE
    # ---------------------------------------------------
    #
    #  These methods are called *by the GUI* when the user finally clicks:
    #    - “Attack” → action_chosen_callback(character, "attack")
    #    - “Sigil” → action_chosen_callback(character, "sigil")
    #    - “Target” → target_chosen_callback(character, target)
    #    - “Sigil” → sigil_chosen_callback(character, sigil)
    #    - “ActiveEffect” → active_effect_chosen_callback(sigil, effect)
    #
    #  Once each of these run, we continue the battle loop in `start_battle`.

    def action_chosen_callback(self, character, action_type):
        """
        GUI calls this once the user chooses “attack” or “sigil”.
        """
        if action_type == "attack":
            self.attack_action(character)
        elif action_type == "sigil":
            self.use_sigil_action(character)

    def target_chosen_callback(self, character, target):
        """
        GUI calls this once the user picks a target after “attack”.
        """
        character.attack_target(target, self)
        # After attacking, go back out of choose_action()
        # (Battle.start_battle loop will handle next character)
      
    def sigil_chosen_callback(self, character, sigil):
        """
        GUI calls this once the user picks a sigil after “use sigil”.
        """
        # Now we must choose which active effect on that sigil
        self.gui_request(
            "choose_active_effect", 
            sigil=sigil, 
            active_effects=sigil.active_effects
        )

    def active_effect_chosen_callback(self, sigil, effect):
        """
        GUI calls this once the user picks an active effect for the chosen sigil.
        """
        # Perform the effect on the equipped character
        character = sigil.equipped_character
        character.activate_active_effect(sigil, effect, self)
        # After using the sigil effect, battle loop continues
