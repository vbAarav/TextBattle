# main.py
import pygame
import time
import character.characters as characters
import players
import map.location as location
import map.area_atlus as area_atlus
import character.character_archive as character_archive

from battle import Battle   # <-- import your new GUI‐ready Battle class


# ──────────────────────────────────────────────────────────────────────────────
#  CONFIGURATION
# ──────────────────────────────────────────────────────────────────────────────
WINDOW_WIDTH, WINDOW_HEIGHT = 800, 600
BG_COLOR           = (20,  20,  20)    # dark background
PANEL_COLOR        = (30,  30,  30)    # slightly lighter for message panel
BUTTON_COLOR       = (50,  50,  50)    # default button color
BUTTON_HOVER       = (70,  70,  70)    # hover color
TEXT_COLOR         = (240, 240, 240)   # light text
INPUT_BG_COLOR     = (40,  40,  40)    # background for text‐entry box
INPUT_BOX_COLOR    = (60,  60,  60)    # border color for text‐entry box
INPUT_TEXT_COLOR   = (255, 255, 255)   # text inside input box

FONT_SMALL  = "Arial"
FONT_MEDIUM = "Arial"
FONT_LARGE  = "Arial"
# ──────────────────────────────────────────────────────────────────────────────


class Button:
    """
    Simple rectangular button with hover effect.
    """
    def __init__(self, rect, text, font, callback):
        """
        rect: pygame.Rect(x, y, w, h)
        text: string to display
        font: pygame.font.Font object
        callback: function to call when clicked
        """
        self.rect     = rect
        self.text     = text
        self.font     = font
        self.callback = callback
        self.hovered  = False

    def draw(self, surface):
        color = BUTTON_HOVER if self.hovered else BUTTON_COLOR
        pygame.draw.rect(surface, color, self.rect, border_radius=5)
        text_surf = self.font.render(self.text, True, TEXT_COLOR)
        text_rect = text_surf.get_rect(center=self.rect.center)
        surface.blit(text_surf, text_rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            self.hovered = self.rect.collidepoint(event.pos)
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                self.callback()


def text_input_screen(screen, clock, prompt, font_prompt, font_input):
    """
    Displays a full‐screen prompt + input box.
    Returns the string entered once Enter is pressed.
    """
    input_text = ""
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if len(input_text.strip()) > 0:
                        return input_text.strip()
                elif event.key == pygame.K_BACKSPACE:
                    input_text = input_text[:-1]
                else:
                    if event.unicode.isprintable():
                        input_text += event.unicode

        screen.fill(BG_COLOR)

        # Render prompt
        prompt_surf = font_prompt.render(prompt, True, TEXT_COLOR)
        prompt_rect = prompt_surf.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 4))
        screen.blit(prompt_surf, prompt_rect)

        # Draw input box
        box_w, box_h = 500, 40
        box_x = (WINDOW_WIDTH - box_w) // 2
        box_y = WINDOW_HEIGHT // 2
        input_box_rect = pygame.Rect(box_x, box_y, box_w, box_h)
        pygame.draw.rect(screen, INPUT_BOX_COLOR, input_box_rect, border_radius=3)
        pygame.draw.rect(screen, INPUT_TEXT_COLOR, input_box_rect, 2, border_radius=3)

        # Render current input text
        txt_surf = font_input.render(input_text, True, INPUT_TEXT_COLOR)
        txt_rect = txt_surf.get_rect(topleft=(box_x + 8, box_y + (box_h - txt_surf.get_height()) // 2))
        screen.blit(txt_surf, txt_rect)

        pygame.display.flip()
        clock.tick(30)


class Game:
    def __init__(self, player, screen):
        self.player    = player
        self.screen    = screen
        self.clock     = pygame.time.Clock()
        self.running   = True

        # game states: "menu", "characters", "inventory", **"battle"**
        self.state     = "menu"

        # Create Map and add starting area
        self.map       = location.Map()
        self.map.add_area(self.player.location)

        # The top “message” panel text
        self.message   = f"You have entered the {self.player.location}."

        # Preload fonts
        self.font_title   = pygame.font.SysFont(FONT_LARGE, 36)
        self.font_button  = pygame.font.SysFont(FONT_MEDIUM, 24)
        self.font_message = pygame.font.SysFont(FONT_SMALL, 20)
        self.font_list    = pygame.font.SysFont(FONT_SMALL, 18)

        # Build main‐menu buttons
        self.buttons = []
        self._create_menu_buttons()

        # “Back” button for sub‐screens
        back_rect = pygame.Rect( WINDOW_WIDTH - 120, WINDOW_HEIGHT - 60, 100, 40 )
        self.back_button = Button(back_rect, "Back", self.font_button, self._on_back)

        # ─────────────────────────────────────────────────────────────────────
        # --- BATTLE‐RELATED FIELDS (new)
        # ─────────────────────────────────────────────────────────────────────
        self.battle            = None
        self.battle_status     = ""     # full text repr of current battle
        self.action_buttons    = []     # e.g. [Attack, Sigil] during “choose_action”
        self.target_buttons    = []     # buttons to pick a target
        self.sigil_buttons     = []     # buttons to pick a sigil
        self.effect_buttons    = []     # buttons to pick a sigil’s active effect
        self.pending_request   = None   # what the Battle is currently waiting for

    def _create_menu_buttons(self):
        margin  = 20
        panel_h = 100
        btn_w   = 300
        btn_h   = 50
        spacing = 15

        x_center = (WINDOW_WIDTH - btn_w) // 2
        y_start  = panel_h + margin

        menu_items = [
            ("Travel To New Location", self._on_travel),
            ("Explore Area",           self._on_explore),
            ("View Characters",        self._on_view_characters),
            ("View Inventory",         self._on_view_inventory),
            ("Quit",                   self._on_quit),
        ]

        for idx, (label, callback) in enumerate(menu_items):
            rect = pygame.Rect(
                x_center,
                y_start + idx * (btn_h + spacing),
                btn_w,
                btn_h
            )
            btn = Button(rect, label, self.font_button, callback)
            self.buttons.append(btn)

    def _draw_message_panel(self):
        panel_rect = pygame.Rect(0, 0, WINDOW_WIDTH, 100)
        pygame.draw.rect(self.screen, PANEL_COLOR, panel_rect)
        lines = self.message.splitlines()
        y_offset = 10
        for line in lines:
            txt_surf = self.font_message.render(line, True, TEXT_COLOR)
            self.screen.blit(txt_surf, (20, y_offset))
            y_offset += txt_surf.get_height() + 5

    # ──────────────────────────────────────────────────────────────────────────
    #  CALLBACKS FOR MAIN MENU BUTTONS
    # ──────────────────────────────────────────────────────────────────────────
    def _on_travel(self):
        new_location = self.map.find_new_location(self.player, self.player.location)
        while new_location is None:
            new_location = self.map.find_new_location(self.player, self.player.location)
        self.player.travel_to(new_location)
        self.message = f"You traveled to {new_location}."

    def _on_explore(self):
        """
        When the player chooses “Explore Area,” we:
        1) call the original explore_area (which should decide if a battle happens),
        2) if a battle should start, it returns an enemy Player instance;
           we then build a Battle(self.player, enemy, self.gui_request) and switch state to “battle”.
        3) otherwise, we just update self.message.
        """
        # Let location.explore_area(...) return either None (no battle)
        # or an enemy Player. You’ll have to modify your existing
        # explore_area(...) to return something like:
        #    return enemy_player
        # when a battle should start.
        enemy_player = self.player.location.explore_area(self.player)

        if enemy_player:
            # Instantiate a GUI‐driven Battle
            self.battle = Battle(self.player, enemy_player, self.gui_request)
            self.state  = "battle"
            self.battle.start_battle()   # <-- this will immediately begin calling gui_request(…)
        else:
            # No enemies found: just show a message
            self.message = f"You explored {self.player.location}, but found nothing."

    def _on_view_characters(self):
        # Switch to “characters” sub‐screen
        self.state = "characters"

    def _on_view_inventory(self):
        # Switch to “inventory” sub‐screen
        self.state = "inventory"

    def _on_quit(self):
        self.message = "Thanks for playing!"
        self._render_once()
        pygame.time.delay(1000)
        self.running = False

    def _on_back(self):
        # Return from sub‐screens to main menu
        self.state   = "menu"
        self.message = "Returned to menu."

    # ──────────────────────────────────────────────────────────────────────────
    #  RENDERING / LOOP LOGIC
    # ──────────────────────────────────────────────────────────────────────────
    def _render_once(self):
        self.screen.fill(BG_COLOR)

        if self.state == "menu":
            self._draw_message_panel()
            for btn in self.buttons:
                btn.draw(self.screen)

        elif self.state == "characters":
            self._draw_characters_screen()

        elif self.state == "inventory":
            self._draw_inventory_screen()

        elif self.state == "battle":
            self._draw_battle_screen()

        pygame.display.flip()

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

                # Dispatch events based on current state
                if self.state == "menu":
                    for btn in self.buttons:
                        btn.handle_event(event)

                elif self.state in ("characters", "inventory"):
                    self.back_button.handle_event(event)

                elif self.state == "battle":
                    # All battle‐related events go to this handler
                    self._handle_battle_event(event)

            self._render_once()
            self.clock.tick(60)

    # ──────────────────────────────────────────────────────────────────────────
    #  CHARACTERS SCREEN
    # ──────────────────────────────────────────────────────────────────────────
    def _draw_characters_screen(self):
        """
        Draws a screen listing each character’s details, plus a “Back” button.
        """
        # 1) Clear background
        self.screen.fill(BG_COLOR)

        # 2) Title bar
        title_surf = self.font_title.render("Characters", True, TEXT_COLOR)
        title_rect = title_surf.get_rect(center=(WINDOW_WIDTH // 2, 40))
        self.screen.blit(title_surf, title_rect)

        # 3) Separator line
        pygame.draw.line(self.screen, TEXT_COLOR, (20, 80), (WINDOW_WIDTH - 20, 80), 2)

        # 4) List each character’s details starting at y = 100
        y = 100
        # Precompute line height once
        line_height = self.font_list.get_height() + 4

        for char in self.player.characters:
            line1 = f"Name:    {char.name}"
            line2 = f"HP:      {char.max_hp}"
            line3 = f"Attack:  {char.attack}"
            line4 = f"Defense: {char.defense}"
            line5 = f"Speed:   {char.speed}"
            line6 = f"Type:    {char.type}"

            for idx, text in enumerate((line1, line2, line3, line4, line5, line6)):
                txt_surf = self.font_list.render(text, True, TEXT_COLOR)
                self.screen.blit(txt_surf, (40, y + idx * line_height))

            # After drawing all 6 lines, move y down by (6 lines + some padding)
            y += 6 * line_height + 15

            # Draw a thin separator between this character and the next
            pygame.draw.line(self.screen, TEXT_COLOR, (20, y - 10), (WINDOW_WIDTH - 20, y - 10), 1)

        # 5) Draw “Back” button
        self.back_button.draw(self.screen)


    # ──────────────────────────────────────────────────────────────────────────
    #  INVENTORY SCREEN
    # ──────────────────────────────────────────────────────────────────────────
    def _draw_inventory_screen(self):
        """
        Draws a screen listing the player's inventory, plus a “Back” button.
        """
        self.screen.fill(BG_COLOR)

        # Title bar
        title_surf = self.font_title.render("Inventory", True, TEXT_COLOR)
        title_rect = title_surf.get_rect(center=(WINDOW_WIDTH // 2, 40))
        self.screen.blit(title_surf, title_rect)

        # Separator line
        pygame.draw.line(self.screen, TEXT_COLOR, (20, 80), (WINDOW_WIDTH - 20, 80), 2)

        # Inventory list starts at y = 100
        y = 100
        inv = self.player.inventory
        if not inv:
            txt_surf = self.font_list.render("Inventory is empty.", True, TEXT_COLOR)
            self.screen.blit(txt_surf, (40, y))
        else:
            for item in inv:
                txt_surf = self.font_list.render(f"- {item}", True, TEXT_COLOR)
                self.screen.blit(txt_surf, (40, y))
                y += self.font_list.get_height() + 6

        # Draw “Back” button
        self.back_button.draw(self.screen)


    # ──────────────────────────────────────────────────────────────────────────
    #  BATTLE SCREEN (NEW)
    # ──────────────────────────────────────────────────────────────────────────
    def _draw_battle_screen(self):
        """
        Draw the current battle status (as text), then any active buttons:
         - If we're waiting on “choose_action”, show Attack / Sigil buttons.
         - If waiting on “choose_target”, show buttons for each character.
         - If waiting on “choose_sigil”, show buttons for each sigil.
         - If waiting on “choose_active_effect”, show buttons for each effect.
         - If battle is over, show winner message & a “Back to Menu” button.
        """
        self.screen.fill(BG_COLOR)

        # --- 1) Draw the “battle status” panel at top
        y_text = 10
        lines = self.battle_status.splitlines()
        for line in lines:
            txt_surf = self.font_list.render(line, True, TEXT_COLOR)
            self.screen.blit(txt_surf, (20, y_text))
            y_text += txt_surf.get_height() + 2

        # --- 2) Draw whichever set of buttons is active
        for btn in self.action_buttons:
            btn.draw(self.screen)
        for btn in self.target_buttons:
            btn.draw(self.screen)
        for btn in self.sigil_buttons:
            btn.draw(self.screen)
        for btn in self.effect_buttons:
            btn.draw(self.screen)

        # --- 3) If the battle is over, draw a “Back” button to return to MENU
        if self.battle and self.battle.get_winner():
            back_rect = pygame.Rect((WINDOW_WIDTH//2 - 75, WINDOW_HEIGHT - 80, 150, 50))
            finish_btn = Button(back_rect, "Back to Menu", self.font_button, self._end_battle_cleanup)
            finish_btn.draw(self.screen)

    def _handle_battle_event(self, event):
        """
        Dispatch Pygame events when in battle state.
        We simply send every mouse event to whichever buttons are currently active.
        """
        # Let any active buttons handle the event:
        for btn in (
            self.action_buttons
            + self.target_buttons
            + self.sigil_buttons
            + self.effect_buttons
        ):
            btn.handle_event(event)

        # If the battle ended and user clicked “Back to Menu”:
        if self.battle and self.battle.get_winner():
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                x, y = event.pos
                # (We know from draw that the back‐to‐menu button is at this rect:)
                back_rect = pygame.Rect((WINDOW_WIDTH//2 - 75, WINDOW_HEIGHT - 80, 150, 50))
                if back_rect.collidepoint((x,y)):
                    self._end_battle_cleanup()

    def _end_battle_cleanup(self):
        """
        Clear all battle‐related fields and return to the main menu.
        """
        self.battle           = None
        self.battle_status    = ""
        self.action_buttons   = []
        self.target_buttons   = []
        self.sigil_buttons    = []
        self.effect_buttons   = []
        self.pending_request  = None
        self.state            = "menu"
        self.message          = "Returned from battle."

    # ──────────────────────────────────────────────────────────────────────────
    #  GUI REQUEST HANDLER
    # ──────────────────────────────────────────────────────────────────────────
    def gui_request(self, request_type, **kwargs):
        """
        This function is passed to Battle(...) as its ‘gui_request’ callback.
        Whenever Battle wants to DISPLAY something or ASK for input, it calls:
            self.gui_request("display_battle_status", status=<string>)
            self.gui_request("pause", duration=<seconds>)
            self.gui_request("choose_action", character=<Character>, can_use_sigil=<bool>)
            self.gui_request("choose_target", character=<Character>, targets=<list of Characters>)
            self.gui_request("choose_sigil", character=<Character>, sigils=<list>)
            self.gui_request("choose_active_effect", sigil=<Sigil>, active_effects=<list>)
            self.gui_request("display_temporary_message", text=<string>)
            self.gui_request("display_winner", winner=<Player>)
        We respond by:
         - updating self.battle_status or other text fields,
         - populating “button lists” so that our render loop shows appropriate buttons,
         - setting `self.pending_request` so that when the user *clicks* a button, we know what to do next.
        """
        # Clear all button lists in preparation for the new request:
        self.action_buttons   = []
        self.target_buttons   = []
        self.sigil_buttons    = []
        self.effect_buttons   = []
        self.pending_request  = request_type

        if request_type == "display_battle_status":
            # kwargs: status (string)
            self.battle_status = kwargs["status"]

        elif request_type == "pause":
            # kwargs: duration (seconds)
            pygame.time.delay(int(kwargs["duration"] * 1000))

        elif request_type == "choose_action":
            # kwargs: character, can_use_sigil (bool)
            char = kwargs["character"]
            can_sigil = kwargs["can_use_sigil"]

            # Make two buttons: “Attack” and (maybe) “Sigil”
            # Position them side by side
            btn_w, btn_h = 200, 40
            x_center = (WINDOW_WIDTH - (btn_w * 2 + 20)) // 2
            y = WINDOW_HEIGHT // 2

            # Attack button
            rect_atk = pygame.Rect(x_center, y, btn_w, btn_h)
            atk_btn = Button(rect_atk, "Attack", self.font_button,
                             lambda: self._action_button_clicked(char, "attack"))
            self.action_buttons.append(atk_btn)

            # Sigil button (only if allowed)
            if can_sigil:
                rect_sigil = pygame.Rect(x_center + btn_w + 20, y, btn_w, btn_h)
                sigil_btn = Button(rect_sigil, "Use Sigil", self.font_button,
                                   lambda: self._action_button_clicked(char, "sigil"))
                self.action_buttons.append(sigil_btn)

        elif request_type == "choose_target":
            # kwargs: character, targets (list of Characters)
            char    = kwargs["character"]
            targets = kwargs["targets"]

            # Display ALL characters in two columns: Allies on left, Enemies on right
            margin_x = 40
            margin_y = 150
            btn_w, btn_h = 200, 30
            spacing   = 10

            # Build a single list of (char, display_text), but we need to know index
            # We will create a button for each c ∈ targets. When clicked, call target_chosen_callback.
            for idx, tgt in enumerate(targets):
                # Stagger buttons vertically
                x = margin_x if tgt in self.battle.get_character_allies(char) else WINDOW_WIDTH//2 + margin_x
                y = margin_y + idx * (btn_h + spacing)//2

                text = f"{tgt.name} (HP: {tgt.hp_current}/{tgt.max_hp})"
                rect = pygame.Rect(x, y, btn_w, btn_h)

                # We need to bind tgt to the callback. Use default arg trick:
                btn = Button(rect, text, self.font_list,
                             lambda tgt=tgt: self._target_button_clicked(char, tgt))
                self.target_buttons.append(btn)

        elif request_type == "choose_sigil":
            # kwargs: character, sigils (list of Sigil)
            sigils = kwargs["sigils"]
            margin_x = 40
            margin_y = 150
            btn_w, btn_h = 300, 30
            spacing   = 10

            for idx, sig in enumerate(sigils):
                x = margin_x
                y = margin_y + idx * (btn_h + spacing)
                text = f"{sig.name}: {sig.description}"
                rect = pygame.Rect(x, y, btn_w, btn_h)

                btn = Button(rect, text, self.font_list,
                             lambda sig=sig: self._sigil_button_clicked(kwargs["character"], sig))
                self.sigil_buttons.append(btn)

        elif request_type == "choose_active_effect":
            # kwargs: sigil, active_effects (list of Effect)
            effects = kwargs["active_effects"]
            margin_x = 40
            margin_y = 150
            btn_w, btn_h = 300, 30
            spacing   = 10

            for idx, eff in enumerate(effects):
                x = margin_x
                y = margin_y + idx * (btn_h + spacing)
                text = f"{eff.name}: {eff.description}"
                rect = pygame.Rect(x, y, btn_w, btn_h)

                btn = Button(rect, text, self.font_list,
                             lambda eff=eff: self._effect_button_clicked(kwargs["sigil"], eff))
                self.effect_buttons.append(btn)

        elif request_type == "display_temporary_message":
            # kwargs: text (string)
            self.message = kwargs["text"]
            # We’ll show it for a short moment; the next battle status usually overwrites it.

        elif request_type == "display_winner":
            # kwargs: winner (Player)
            winner = kwargs["winner"]
            self.battle_status = f"Battle Over! Winner: {winner.name}"
            # We keep self.state == "battle" so that the “Back to Menu” button appears.

        else:
            # Unknown request_type
            pass

    # ──────────────────────────────────────────────────────────────────────────
    #  BUTTON‐CLICK CALLBACKS (when the player finally clicks in battle UI)
    # ──────────────────────────────────────────────────────────────────────────
    def _action_button_clicked(self, character, action_type):
        """
        Called when the player clicks “Attack” or “Use Sigil” after gui_request("choose_action").
        We forward to battle.action_chosen_callback(...)
        """
        # Clear these buttons so the next gui_request can repaint
        self.action_buttons = []
        self.battle.action_chosen_callback(character, action_type)

    def _target_button_clicked(self, character, target):
        """
        Called when the player clicks on a target after gui_request("choose_target").
        """
        self.target_buttons = []
        self.battle.target_chosen_callback(character, target)

    def _sigil_button_clicked(self, character, sigil):
        """
        Called when the player clicks on a sigil after gui_request("choose_sigil").
        """
        self.sigil_buttons = []
        self.battle.sigil_chosen_callback(character, sigil)

    def _effect_button_clicked(self, sigil, effect):
        """
        Called when the player clicks on an active effect after gui_request("choose_active_effect").
        """
        self.effect_buttons = []
        self.battle.active_effect_chosen_callback(sigil, effect)


if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("TextBattle → PyGame Edition")

    # ──────────────────────────────────────────────────────────────────────────
    #  1) Enter Player Name (GUI)
    # ──────────────────────────────────────────────────────────────────────────
    clock = pygame.time.Clock()
    font_prompt = pygame.font.SysFont(FONT_LARGE, 36)
    font_input  = pygame.font.SysFont(FONT_MEDIUM, 24)
    player_name = text_input_screen(
        screen,
        clock,
        "Enter your name:",
        font_prompt,
        font_input
    )

    player = players.Player(player_name, location=area_atlus.LONG_PLAINS)

    # ──────────────────────────────────────────────────────────────────────────
    #  2) Enter Character Name (GUI)
    # ──────────────────────────────────────────────────────────────────────────
    character_name = text_input_screen(
        screen,
        clock,
        "Enter your character's name:",
        font_prompt,
        font_input
    )

    template = character_archive.MC_TEMPLATE
    template.name = character_name
    template.type = characters.Colour.random_type()
    character = characters.Character(
        character_name,
        max_hp=100,
        attack=3,
        defense=1,
        speed=1,
        type=characters.Colour.random_type()
    )
    player.characters.append(character)

    print(f"{character.name} has entered the world!\n")
    time.sleep(1)

    # ──────────────────────────────────────────────────────────────────────────
    #  3) Launch the Main Menu (GUI Buttons + Message Panel)
    # ──────────────────────────────────────────────────────────────────────────
    game = Game(player, screen)
    game.run()

    pygame.quit()
    print("Exited PyGame. Goodbye!")
