from kivy.properties import StringProperty
from kivy.uix.screenmanager import Screen
from kivy.app import App
from kivy.uix.popup import Popup

from elements import Campaign


# Campaign
class CampaignsListWindow(Screen):
    """
    Campaigns list
    """
    pass


class CampaignDetailsWindow(Screen):
    """
    Campaigns list
    """
    pass


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
