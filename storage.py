# same file for players and games as separate entries
from typing import List, Any

# get players from here and send to Table by caller

from kivy.app import App
import json
from pathlib import Path
import os
from elements import Player, Reinforcements, Faction, Campaign


class Data:
    def __init__(self):
        #Default players
        self.players = [Player(f"Player {_+1}") for _ in range(4)]

        # toDO: save and load card rename base - changes to popup

        # Default factions
        self.factions = [
            # Core box
            Faction("Rebel", "Core"),
            Faction("Empire","Core",True),

            # Clone Wars box
            Faction("Republic", "Clone Wars"),
            Faction("Separatists","Clone Wars",True),

            # Mandalorian Expansion
            Faction("Mandalorian","Mandalorian"),
        ]

        # Default reinforcements
        self.reinforcements = [
            # Rebel & Empire Reinforcements Expansion
            Reinforcements(self.factions[0].name), Reinforcements(self.factions[1].name)]

        # Default neutral decks
        self.neutral = [
            self.factions[0].box,
            self.factions[2].box,
        ]

        # All campaigns list
        self.campaigns: List[Campaign] = []

    @staticmethod
    def file_path() -> str:
        """
        Gets running app instance and specifies file path
        :
        :return: file path
        """
        # App instance
        app = App.get_running_app()
        data_dir = app.user_data_dir

        # file path
        json_file = os.path.join(data_dir, "settings.json")
        return json_file

    def load_file(self) -> None:
        """Reads saved file if it exists, then set saved players names"""

        json_file = self.file_path()

        # Check if file exists
        if Path(json_file).exists():
            try:
                # open file
                with open(json_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    # rebuild this structure for campaign mode
                    # Set players
                    print(f"Loading data from file:\n {data}")

                    self.dict_to_data(data)

            except json.decoder.JSONDecodeError:
                return None

        return None

    def save_file(self):
        """
        Serialize data to JSON and save it to a file.

        The function determines the target file path using ``file_path()``
        and writes the provided data object to the file in JSON format.
        Existing content will be overwritten."""

        with open(self.file_path(), "w", encoding="utf-8") as f:
            data = self.data_to_dict()
            json.dump(data, f,indent=4, ensure_ascii=False)

            print(self.file_path())

    def get_players(self):
        # return players
        return self.players

    def update_players(self, players_names: list[str]):
        """Gets list of the players names and assign it as a new names for the players.
        If name is empty, set it to default name "Player X"."""

        for name, player in zip(players_names, self.players):
            # Check if name is empty
            if not name or name.strip() == "":
                name = f"Player {self.players.index(player)+1}"

            # Rename player
            player.rename(name)

    def new_campaign(self, players: List[Player]):
        """Creates new campaign and assign it to the beginning of campaign list, then saves it.
        :param players: list of Players instances
        """
        campaign = Campaign(players)

        # new campaign first
        self.campaigns.insert(0, campaign)
        # save
        self.save_file()

    def save_campaign(self):
        """Saves current campaign to file, based on app variables selected_campaign and working_campaign.
        Saved campaign will be moved to the beginning of campaign list."""
        app = App.get_running_app()

        new = app.working_campaign
        old = app.selected_campaign

        # insert campaign to the list
        self.campaigns.insert(0, new)
        # remove original instance
        self.campaigns.remove(old)
        # save the file
        self.save_file()

        # Create new base
        old = new
        app.prepare_working_campaign(old)

    def players_to_dict(self) -> dict[str, str]:
        """
        Returns a dictionary of players names .
        """
        pl_names = {f"player{i+1}": self.players[i].name for i in range(len(self.players))}

        return pl_names

    def data_to_dict(self) -> dict[str, dict[str, Any]]:
        """Converts stored data object to a dictionary."""

        players = {"players": self.players_to_dict()}
        factions = {"factions": [faction.to_dict() for faction in self.factions]}
        campaign = {"campaigns": [campaign.to_dict() for campaign in self.campaigns]}

        return players | factions | campaign

    def dict_to_data(self, data):
        """Converts data dictionary to Data() stored objects.
        :param data: data dictionary
        """

        # Players names
        self.update_players(data["players"].values())
        #Factions
        self.factions = [Faction.from_dict(faction) for faction in data["factions"]]
        # Campaign
        # skip if list is empty
        if data["campaigns"]:
            self.campaigns = [Campaign.from_dict(campaign) for campaign in data["campaigns"]]
