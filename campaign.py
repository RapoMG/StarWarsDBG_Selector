from copy import deepcopy
from itertools import zip_longest

from kivy.core.window import Window
from kivy.properties import StringProperty, NumericProperty, BooleanProperty, ObjectProperty
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.relativelayout import RelativeLayout

from kivy.uix.screenmanager import Screen
from kivy.uix.popup import Popup
from kivy.uix.label import Label

from functools import partial
from kivy.app import App
from kivy.clock import Clock
from kivy.metrics import dp


from elements import Campaign, Player, Faction, Reinforcements

# Functions and buttons
class CampaignButton(ButtonBehavior, FloatLayout):
    """
    Properties for button collecting values of campaign variables
    """
    game = StringProperty("")

    p1_name = StringProperty("")
    p1_faction_image = StringProperty("")

    p1_reinforcements = StringProperty("")

    p2_name = StringProperty("")
    #p2_faction = StringProperty("")
    p2_faction_image = StringProperty("")
    p2_reinforcements = StringProperty("")


class DeleteBtn(Button):
    pass


class EditableArea(ButtonBehavior, GridLayout):
    editable = BooleanProperty(False)
    owner = ObjectProperty(None)
    action = StringProperty("")

    def on_release(self):
        if not self.editable:
            return
        if self.owner:
            self.owner.popup_selector(self.action, self)


class StarterCardsRow(BoxLayout):
    card_name = StringProperty("")
    value = NumericProperty(0)
    source_dict = ObjectProperty(None)

    def increase(self):
        self.value += 1
        self.source_dict[self.card_name] = self.value

    def decrease(self):
        if self.value > 0:
            self.value -= 1
            self.source_dict[self.card_name] = self.value


class StarterDeckRow(GridLayout):
    """
    Properties for row displaying starter cards in order:
    faction1 card, quantity, faction2 card, quantity
    """
    p1_card_name = StringProperty("")
    p1_card_nbr = StringProperty("")

    p2_card_name = StringProperty("")
    p2_card_nbr = StringProperty("")


class ErrorsRow(GridLayout):
    error = StringProperty("")


def ordinal_numbers(game_number: int) -> str:
    """Converts game number to ordinal number in range 1-5. Numbers above the rage are converted to string type."""
    numeral_words = ["First", "Second", "Third", "Fourth", "Fifth"]
    if game_number > 5:
        word = str(game_number)
    else:
        word = numeral_words[game_number - 1]
    return word


# Campaign windows
class CampaignsListWindow(Screen):
    """
    Screen displaying campaigns list as buttons.
    Each button is linked to a campaign instance and opens CampaignDetailsWindow.
    """

    campaigns = None

    def on_pre_enter(self):

        app = App.get_running_app()

        self.campaigns = app.data.campaigns
        # campaigns = self.campaigns

        button_grid = self.ids.campaigns
        button_grid.clear_widgets()

        for campaign in self.campaigns:
            # Create a container for the campaign button and the delete button
            row = BoxLayout(size_hint_y=None, height=dp(120), spacing=30, padding=(dp(25),0,dp(10),dp(2)))

            campaign_button = CampaignButton(
                game=ordinal_numbers(campaign.game),

                p1_name=campaign.players[0].name,
                p1_faction_image=self.faction_name(campaign.players[0].faction.name),
                p1_reinforcements=campaign.players[0].reinforcements.faction_name,

                p2_name=campaign.players[1].name,
                p2_faction_image=self.faction_name(campaign.players[1].faction.name),
                p2_reinforcements=campaign.players[1].reinforcements.faction_name,
            )

            campaign_button.bind(on_release=partial(self.campaign_selection, campaign))

            # Smaller delete button
            delete_btn = DeleteBtn()
            delete_btn.bind(on_release=partial(self.confirm_delete, campaign))

            row.add_widget(campaign_button)
            row.add_widget(delete_btn)
            button_grid.add_widget(row)

    def confirm_delete(self, campaign, instance):
        popup = DeleteCampaignPopup(campaign=campaign, on_confirm=self.delete_campaign)
        popup.open()

    def delete_campaign(self, campaign):
        app = App.get_running_app()
        if campaign in app.data.campaigns:
            app.data.campaigns.remove(campaign)
            app.data.save_file()
            self.on_pre_enter()  # Refresh the list

    def campaign_selection(self, campaign, instance):
        """
        Action for dynamically generated campaign buttons.
        Method takes Campaign instance as an argument and assigns it to app level variable,
        then switch to different screen, where it will be used.
        """
        app = App.get_running_app()
        # app.selected_campaign = campaign

        #prepare working campaign
        app.prepare_working_campaign(campaign)

        self.manager.current = "campaign_details"

    def faction_name(self,faction_name: str) -> str:
        """
        Returns faction image depending on chosen name.
        :param faction_name: name of faction
        :type: string,
        :return: string.
        """


        image = {
            "Rebel": "images/fact_buttons/reb_on.png",
            "Empire": "images/fact_buttons/emp_on.png",
            "Republic": "images/fact_buttons/rep_on.png",
            "Separatists": "images/fact_buttons/sep_on.png",
            "Mandalorian": "images/fact_buttons/mand_on.png",
        }

        # Placeholder implementation - replace with actual faction image paths
        return image.get(faction_name, "images/icon.png")

class CampaignDetailsWindow(Screen):
    """
    Campaigns list
    """
    game_number = StringProperty("")

    campaign = None

    editable = BooleanProperty(False)  # switch between view and edit Screen

    main_button_text = StringProperty("Resolve the Battle")

    def on_pre_enter(self, *args):
        app = App.get_running_app()

        if app.working_campaign is None:
            app.prepare_working_campaign(app.selected_campaign)

        self.campaign = app.working_campaign

        self.game_number = ordinal_numbers(self.campaign.game)

        # Player 1 headers
        self.ids.player1.text = self.campaign.players[0].name
        self.ids.faction1.text = self.campaign.players[0].faction.name
        self.ids.rein1.text = self.campaign.players[0].reinforcements.faction_name

        # Player 2 headers
        self.ids.player2.text = self.campaign.players[1].name
        self.ids.faction2.text = self.campaign.players[1].faction.name
        self.ids.rein2.text = self.campaign.players[1].reinforcements.faction_name

        self.ids.rules_warning.opacity = 0 if self.campaign.matching_factions() else 1
        self.ids.rules_warning2.opacity = 0 if self.campaign.matching_factions() else 1
        self.ids.main_button.opacity = 0 if self.campaign.game == 5 else 1

        # Starter dacks
        self.populate_card_rows(self.ids.starter_cards, self.campaign.players_deck(1), self.campaign.players_deck(2))

        # Removed galaxy cards
        self.populate_card_rows(self.ids.removed_cards, self.campaign.p1_removed_cards, self.campaign.p2_removed_cards)

        # Added galaxy cards
        self.populate_card_rows(self.ids.added_cards, self.campaign.p1_added_cards, self.campaign.p2_added_cards)

        # Removed bases
        self.populate_card_rows(self.ids.removed_bases, self.campaign.p1_removed_bases, self.campaign.p2_removed_bases)

        # Set extra resource for the second player
        self.resource(app) # move that to campaign creation stage

    def primary_action(self):
        """Defines action for Screen primary button depending on the current screen mode (edit | errors | display)."""

        # After fifth (last) game
        if self.campaign.game == 5:
            if __name__ == '__main__':
                self.ids.main_button.hidden = True
                self.ids.main_button.disabled = True
                self.ids.main_button.opacity = 0
        # is in display mode
        elif not self.editable:
            # switch to edit mode
            self.edit_mode(True)
            print("primary action made it editable")

        # edit mode but with errors
        elif self.has_errors(): # assigns errors to dict and return bool
            #self.show_errors_popup() # calls popup list
            print("primary action see it has errors")
            popup = DeckErrorsPopup()

            popup.open()

        # edit mode and no errors
        else:
            # turn off edit mode
            self.edit_mode(False)

            # Increase game number
            self.campaign.game += 1

            # save campaign
            app = App.get_running_app()
            app.data.save_campaign()

            self.refresh_screen()

        self.update_main_button()

    def refresh_screen(self):
        """After saving game reloads data to display"""
        app = App.get_running_app()
        self.campaign = app.working_campaign
        self.game_number = ordinal_numbers(self.campaign.game)

    def update_main_button(self, *args):
        """Text and color for the main button depending on the current screen mode (edit | errors | display)."""
        # is in display mode
        if not self.editable:
            #print("display text")
            self.main_button_text = "Resolve the Battle"
            self.ids.main_button.color = "yellow"

        # edit mode but with errors
        elif self.has_errors():
            #print("errors text")
            self.main_button_text = "Show decks errors"
            self.ids.main_button.color = "red"
        else:
            #print("confirm text")
            self.main_button_text = "Confirm Reinforcements"
            self.ids.main_button.color = "green"

    def edit_mode(self,edit: bool = False):

        disabled = not edit

        # change state to editable mode
        self.editable = edit

        # Editions area
        self.ids.starter_cards_area.editable = edit
        self.ids.removed_cards_area.editable = edit
        self.ids.added_cards_area.editable = edit
        self.ids.removed_bases_area.editable = edit

        # Force fields
        self.ids.p1_resource.disabled = disabled

        self.ids.force_2.disabled = disabled

        # Force buttons
        self.ids.force_3.disabled = disabled
        self.ids.force_n.disabled = disabled
        self.ids.force_5.disabled = disabled
        self.ids.force_6.disabled = disabled
        self.ids.p2_resource.disabled = disabled

    def resource(self, app):
        """
        Draws first player
        """
        pl = self.campaign.players

        self.ids.p1_resource.state = "normal" if pl[0].first else "down"
        self.ids.p2_resource.state = "normal" if pl[1].first else "down"

        print(F"p1: {pl[0].first}, p2: {pl[1].first}")

    def schedule_button_update(self, *args):
        Clock.schedule_once(self.update_main_button, 0)

    def popup_selector(self, action: str, instance=None):

        if action == "starter cards":
            print("starter cards")

            popup = StarterCardsPopup()
            popup.faction1 = self.campaign.players[0].faction.name
            popup.faction2 = self.campaign.players[1].faction.name

            popup.bind(on_dismiss=partial(self.refresh_starter, action))
            popup.bind(on_dismiss=self.schedule_button_update)

            popup.open()

        else:
            popup = AddCardTablePopup()

            popup.action = action
            popup.faction1 = self.campaign.players[0].faction.name
            popup.faction2 = self.campaign.players[1].faction.name

            hints = {
                "removed cards": "Name card to remove",
                "added cards": "Name card to add",
                "removed bases": "Name base to remove",
            }

            popup.ids.faction1_card.hint_text = hints.get(action, "Card name")
            popup.ids.faction2_card.hint_text = hints.get(action, "Card name")

            popup.bind(on_dismiss=partial(self.update_card_list, action))
            popup.bind(on_dismiss=self.schedule_button_update)

            popup.open()

    def refresh_starter(self, action, popup):
        if action != "starter cards":
            return
        self.populate_card_rows(self.ids.starter_cards, self.campaign.players_deck(1), self.campaign.players_deck(2))

    def update_card_list(self, action: str, popup):
        """
        Update the name of a card in the list.
        Add cards from the popup inputs to the campaign list selected by action.

        :param action: string representing the action
        :param popup: Instance of Popup

        """
        lists_by_action = {
            "removed cards": (
                self.campaign.p1_removed_cards,
                self.campaign.p2_removed_cards,
                self.ids.removed_cards,
                "Name card to remove",
            ),
            "added cards": (
                self.campaign.p1_added_cards,
                self.campaign.p2_added_cards,
                self.ids.added_cards,
                "Name card to add",
            ),
            "removed bases": (
                self.campaign.p1_removed_bases,
                self.campaign.p2_removed_bases,
                self.ids.removed_bases,
                "Name base to remove",
            ),
        }

        selected_lists = lists_by_action.get(action)
        if selected_lists is None:
            return

        p1_cards, p2_cards, container, hint = selected_lists

        self.add_card_copy(p1_cards, popup.ids.faction1_card.text)
        self.add_card_copy(p2_cards, popup.ids.faction2_card.text)

        self.populate_card_rows(container, p1_cards, p2_cards)

    @staticmethod
    def add_card_copy(cards: dict[str, int], card_name: str):
        card_name = card_name.strip()
        if card_name == "":
            return

        cards[card_name] = cards.get(card_name, 0) + 1

    @staticmethod
    def populate_card_rows(container_id, p1_column: dict[str, int], p2_column: dict[str, int]):
        """
        Populates the starter decks rows with card names and quantities for both players.
        :param container_id: id of layout container displaying cards
        :param p1_column: Dictionary of card names and quantities for player 1
        :param p2_column: Dictionary of card names and quantities for player 2
        """
        container_id.clear_widgets()

        # Starter decks rows number
        container_id.rows = max(len(p1_column), len(p2_column))

        # Starter decks rows
        for p1_card, p2_card in zip_longest(p1_column, p2_column, fillvalue=""):
            row = StarterDeckRow(
                p1_card_name=p1_card,
                p1_card_nbr=str(p1_column.get(p1_card)) if p1_card else "",

                p2_card_name=p2_card,
                p2_card_nbr=str(p2_column.get(p2_card)) if p2_card else "",
            )

            container_id.add_widget(row)

    def has_errors(self) -> bool:
        """Calls campaign validator
        :return: True if campaign decks are valid, False otherwise
        """
        errors = self.campaign.campaign_valid()
        return bool(errors)

    def exit_cleanup(self):
        """Setups properties to default values"""
        self.populate_card_rows(self.ids.starter_cards, {}, {})
        self.populate_card_rows(self.ids.removed_cards, {}, {})
        self.populate_card_rows(self.ids.added_cards, {}, {})
        self.populate_card_rows(self.ids.removed_bases, {}, {})

        App.get_running_app().clear_working_elements()


class NewCampaignWindow(Screen):
    """
    New campaign
    """
    players = []
    factions = []
    reinforcements = []

    def on_pre_enter(self):
        app = App.get_running_app()

        app.prepare_working_elements()

        self.players = [app.pl_working[0], app.pl_working[1]] # 2 players in campaign
        self.factions = app.fc_working
        self.reinforcements = app.rein_working

        self.update_status()

    def update_status(self):
        # WIDGET TEXT
        # Players
        self.ids.player1.text = self.players[0].name
        self.ids.player2.text = self.players[1].name

        # Factions
        if self.players[0].faction is not None:
            self.ids.faction1.text = self.players[0].faction.name
        if self.players[1].faction is not None:
            self.ids.faction2.text = self.players[1].faction.name

        # Reinforcements
        if self.players[0].reinforcements is not None:
            self.ids.exp_faction1.text = self.players[0].reinforcements.faction_name
        if self.players[1].reinforcements is not None:
            self.ids.exp_faction2.text = self.players[1].reinforcements.faction_name


        self.ids.rules_warning.opacity = 0

        # all fields used validation
        if (self.players[0].reinforcements is not None and self.players[1].reinforcements is not None
                and self.players[0].faction is not None and self.players[1].faction is not None):

            # Rules warning display
            if (self.players[0].faction.name != self.players[0].reinforcements.faction_name
                and self.players[1].faction.name != self.players[1].reinforcements.faction_name):

                self.ids.rules_warning.opacity = 1

            # Start campaign display / no duplicates validator
            if (self.players[0].faction.name != self.players[1].faction.name
                and self.players[0].reinforcements.faction_name != self.players[1].reinforcements.faction_name):

                self.ids.start.opacity = 1

    def chose_faction(self, player_index):

        # other player index
        other = 1 if player_index == 0 else 0

        if self.players[other].faction is not None:
            available_factions = [faction.name for faction in self.factions if
                              faction.name != self.players[other].faction.name]
        else:
            available_factions = [faction.name for faction in self.factions]

        # If any faction is not available, add an empty string
        if len(available_factions) == 4:
            available_factions.append("")

        popup = SelectFactionPopup(
            field1=available_factions[0],
            field2=available_factions[1],
            field3=available_factions[2],
            field4=available_factions[3],
            field5=available_factions[4],

        )

        popup.bind(on_dismiss=lambda *_: self._apply_faction_selection(popup.selected_faction, player_index))
        popup.open()

    def _apply_faction_selection(self, faction_name:str, player_index: int):
        """
        Applies selected faction to player basing on name of a chosen faction.
        :param faction_name: faction name
        :param player_index: player index"""
        if not faction_name:
            return

        for faction in self.factions:
            if faction.name == faction_name:
                self.players[player_index].add_faction(faction)
                break

        self.update_status()

    def chose_reinforcements(self, player_index):

        # other player index
        other = 1 if player_index == 0 else 0

        popup = SelectFactionPopup(
            field1=self.reinforcements[0].faction_name,
            field2=self.reinforcements[1].faction_name,
            field3="",
            field4="",
            field5="",

        )

        popup.bind(on_dismiss=lambda *_: self._apply_rein_selection(popup.selected_faction, player_index, other))
        popup.open()

    def _apply_rein_selection(self, rein_name, player_index, other):

        if not rein_name:
            return

        for rein in self.reinforcements:
            if rein.faction_name == rein_name:
                self.players[player_index].add_reinforcements(rein)
            else:
                self.players[other].add_reinforcements(rein)

        self.update_status()

    def start_campaign(self):
        """Draws the first player and creates a new campaign instance, then saves it to the file."""

        app = App.get_running_app()
        pl = self.players

        # Re-use Game table
        t = deepcopy(app.table)  # Call game table module
        t.names = pl  # Set players names
        t.nbr_of_players(len(pl))  # Number of players
        t.players2()  # draw first player

        app.data.new_campaign(pl)

        new = app.data.campaigns[0]

        app.prepare_working_campaign(new)

    def clean_fields(self):
        """Restores screen to entry view, and removes working instances of the game elements."""
        self.ids.faction1.text = "Select faction"
        self.ids.faction2.text = "Select faction"
        self.ids.exp_faction1.text = "Reinforcements"
        self.ids.exp_faction2.text = "Reinforcements"

        App.get_running_app().clear_working_elements()


class SelectFactionPopup(Popup):

    field1 = StringProperty("")
    field2 = StringProperty("")
    field3 = StringProperty("")
    field4 = StringProperty("")
    field5 = StringProperty("")

    selected_faction = StringProperty("")

    def assign_faction(self, faction_name: str):
        self.selected_faction = faction_name
        self.dismiss()


class AddCardTablePopup(Popup):

    action = StringProperty("")

    faction1 = StringProperty("")
    faction2 = StringProperty("")

    faction1_card = StringProperty("")
    faction2_card = StringProperty("")


class StarterCardsPopup(Popup):

    faction1 = StringProperty("")
    faction2 = StringProperty("")

    def on_open(self):
        app = App.get_running_app()
        campaign = app.working_campaign

        self.populate(self.ids.player1_grid, campaign.p1_start)
        self.populate(self.ids.player2_grid, campaign.p2_start)

    def populate(self, grid, data):
        grid.clear_widgets()

        for card_name, amount in data.items():
            row = StarterCardsRow(
                card_name=card_name,
                value=amount,
                source_dict=data
            )
            grid.add_widget(row)


class DeckErrorsPopup(Popup):

    def on_open(self):
        app = App.get_running_app()
        errors = app.working_campaign.campaign_valid()
        print(f"in popup:{errors}")

        errors_grid = self.ids.errors_grid

        errors_grid.clear_widgets()

        for faction, deck, diff in errors:

            direction = "has too many" if diff > 0 else "doesn't have enough"
            line = Label(
                text=f"{faction} faction {direction} {deck} cards.",
                color="red",
                size_hint_y=None,
                height=40,
            )

            errors_grid.add_widget(line)


class DeleteCampaignPopup(Popup):
    def __init__(self, campaign, on_confirm, **kwargs):
        super().__init__(**kwargs)
        self.title_size = 0  # no title line
        self.separator_height = 0  # no separator line
        self.size_hint = (0.8, 0.4)

        text="Hello there!\nAre you sure you want to delete this campaign?\nArchives may become incomplete."

        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        layout.add_widget(Label(text=text))

        buttons = BoxLayout(spacing=10, size_hint_y=None, height=dp(50))

        yes_btn = Button(text="Yes")
        yes_btn.bind(on_release=lambda x: [on_confirm(campaign), self.dismiss()])

        no_btn = Button(text="No")
        no_btn.bind(on_release=self.dismiss)

        buttons.add_widget(yes_btn)
        buttons.add_widget(no_btn)
        layout.add_widget(buttons)

        self.content = layout
