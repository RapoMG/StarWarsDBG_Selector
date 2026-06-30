from itertools import zip_longest

from kivy.properties import StringProperty, NumericProperty, BooleanProperty, ObjectProperty
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout

from kivy.uix.screenmanager import Screen
from kivy.uix.popup import Popup
from kivy.uix.label import Label

from functools import partial
from kivy.app import App

from elements import Campaign, Player, Faction, Reinforcements
#from table import Table


# Functions and buttons
class CampaignButton(ButtonBehavior, FloatLayout):
    """
    Properties for button collecting values of campaign variables
    """
    game = StringProperty("")

    p1_name = StringProperty("")
    p1_faction = StringProperty("")
    p1_reinforcements = StringProperty("")

    p2_name = StringProperty("")
    p2_faction = StringProperty("")
    p2_reinforcements = StringProperty("")

class EditableArea(ButtonBehavior, GridLayout):
    editable = BooleanProperty(False)
    owner = ObjectProperty(None)
    action = StringProperty("")

    def on_release(self):
        if not self.editable:
            print("behavior turned off")
            return
        if self.owner:
            self.owner.popup_selector(self.action, self)
            #self.open_popup(self) #Or local function

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
    Properties for starter deck row
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
    Campaigns list
    """
    ## Temporary tests code ##
    test_player = Player("Maciejka")

    test_player.add_faction(Faction("Rebelia"))
    test_player.add_reinforcements(Reinforcements("Rebelianci"))

    test_player2 = Player("Maciek")

    test_player2.add_faction(Faction("Empire"))
    test_player2.add_reinforcements(Reinforcements("Stormtroopers"))

    test_campaign = Campaign(
        [test_player, test_player2]
    )

    test_campaign2 = Campaign(
        [test_player2, test_player]
    )
    ##########
    campaigns = [test_campaign, test_campaign2]

    def on_pre_enter(self):

        #app = App.get_running_app()

        #campaigns = app.data.campaigns
        campaigns = self.campaigns

        button_grid = self.ids.campaigns
        button_grid.clear_widgets()

        print(len(campaigns))

        for campaign in campaigns:
            campaign_button = CampaignButton(
                game=ordinal_numbers(campaign.game),

                p1_name=campaign.players[0].name,
                p1_faction=campaign.players[0].faction.name,
                p1_reinforcements=campaign.players[0].reinforcements.faction_name,

                p2_name=campaign.players[1].name,
                p2_faction=campaign.players[1].faction.name,
                p2_reinforcements=campaign.players[1].reinforcements.faction_name,
            )

            campaign_button.bind(on_release=partial(self.campaign_selection, campaign))

            button_grid.add_widget(campaign_button)

    def campaign_selection(self, campaign, instance):
        """
        Action for dynamically generated campaign buttons.
        Method takes Campaign instance as an argument and assigns it to app level variable,
        then switch to different screen, where it will be used.
        """
        app = App.get_running_app()
        app.selected_campaign = campaign

        self.manager.current = "campaign_details"

    # ToDO: delete campaign button


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
        self.campaign = app.selected_campaign

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

        # Starter dacks
        self.populate_card_rows(self.ids.starter_cards, self.campaign.players_deck(1), self.campaign.players_deck(2))

        # Todo: Remove those fakes after tests
        self.campaign.p1_removed_cards.update({"Yoda": 1})
        self.campaign.p1_added_cards.update({"Darth Maul": 1})
        self.campaign.p2_removed_bases.update({"dagobah": 1, "Illum": 1})

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

        # is in display mode
        if not self.editable:
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
            # Refresh data?
                # add +1 to battle number
            # save campaign
            app = App.get_running_app()
            #ToDo: Create saving method
            #app.data.save_campaign()

        self.update_main_button()

    def update_main_button(self, *args):
        """Text and color for the main button depending on the current screen mode (edit | errors | display)."""
        #print("buton text outer")
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

        # ToDo: Update here?
        #self.update_main_button()


        # ToDo:
        #  Battle results changed to accept button
        #       on_release: calls save campaign method in Data
        #       Turn off edit
        #       Add +1 to battle number
        #       After confirming 5th battle counter displays "campaign finished" and disables all buttons
        #  clean after leaving to camp selection

    def resource(self, app):
        """
        Draws first player
        """
        pl = self.campaign.players
        #pl[0].first=True
        # Todo: add check if players have first already set and move draw to new campaign creation screen
        t = app.table
        t.names = pl
        t.players2()
        self.ids.p1_resource.state = "normal" if pl[0].first else "down"
        self.ids.p2_resource.state = "normal" if pl[1].first else "down"

        print(F"p1: {pl[0].first}, p2: {pl[1].first}")

    def popup_selector(self, action: str, instance=None):

        if action == "starter cards":
            print("starter cards")

            popup = StarterCardsPopup()
            popup.faction1 = self.campaign.players[0].faction.name
            popup.faction2 = self.campaign.players[1].faction.name

            #popup.bind(on_dismiss=lambda *_: self.refresh_starter())
            popup.bind(on_dismiss=partial(self.refresh_starter, action))
            popup.bind(on_dismiss=self.update_main_button)

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

            # ToDo: Update button here?
            popup.bind(on_dismiss=self.update_main_button)

            #popup.bind(text=partial(self.update_card_list,action))
            #popup.bind(text=partial(self.update_card_list,action, deck, i))

            popup.open()

    def refresh_starter(self, action, popup):
        if action != "starter cards":
            return
        self.populate_card_rows(self.ids.starter_cards, self.campaign.players_deck(1), self.campaign.players_deck(2))

    def update_card_list(self, action, popup):
        """
        Update the name of a card in the list.

        :param deck: Class Faction or Reinforcements
        :param index: Index of the card to update
        :param widget: TextInput widget
        :param text: New text for the card
        """
       # # if:
       #  deck.rename_card(index, text)

        # if action == "starter cards":
        #     print("starter cards")
        # elif action == "removed cards":
        #     print("removed cards")
        #     # chack if card is already on the list
        #     card1_q = self.campaign.p1_removed_cards.get(text)
        #     if card1_q is None:
        #         card1_q = 0
        #     # Add copy of card
        #     self.campaign.p1_removed_cards.update({text: card1_q+1})
        #
        #     # self.p1_removed_cards: Dict[str, int] = {}
        #     # self.p2_removed_cards: Dict[str, int] = {}
        # elif action == "added cards":
        #     print("added cards")
        # elif action == "removed bases":
        #     print("removed bases")

        """
        Add cards from the popup inputs to the campaign list selected by action.
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
        #starters = self.ids.starter_cards
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
        # Todo: clean this screen,
        #  made temporary campaign variable (copy) to work on
        #  save: overwrite original


class NewCampaignWindow(Screen):
    """
    New campaign
    """
    players = []
    factions = []
    reinforcements = []

    def on_pre_enter(self):
        app = App.get_running_app()

        self.players = app.data.get_players()
        self.factions = app.fc
        self.reinforcements = app.rein

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

        #available_factions = [faction.name for faction in self.factions if faction.name not in self.players[other].faction]
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


    def _apply_faction_selection(self, faction_name, player_index):

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
        app = App.get_running_app()
        app.data.new_campaign(self.players)

    def clean_fields(self):
        self.ids.faction1.text = "Select faction"
        self.ids.faction2.text = "Select faction"
        self.ids.exp_faction1.text = "Reinforcements"
        self.ids.exp_faction2.text = "Reinforcements"


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
        campaign = app.selected_campaign

        # ToDO: add method to both decks access

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
        errors = app.selected_campaign.campaign_valid()
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

# ToDo: Starter Popup
#    Confirm button is available if campaign validators ar ok (make working validators)
#    updates game number (bind on popup like 272, 292 ?
#    saves game (make class to dict, and dict to class)
#
#
