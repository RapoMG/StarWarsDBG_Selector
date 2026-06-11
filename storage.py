# same file for players and games as separate entries

# get players from here and send to Table by caller

from kivy.app import App
import json
from pathlib import Path
import os
from elements import Player

class Data:
    def __init__(self):
        #Default players
        self.players = [Player(f"Player {_+1}") for _ in range(4)]

    @staticmethod
    def file_path() -> str:
        """
        Gets running app instance and specifies file path
        return: file path
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
                    names = data.values()
                    self.update_players(names)

            except json.decoder.JSONDecodeError:
                return None

        return None

    def save_file(self):
        """
        Serialize data to JSON and save it to a file.

        The function determines the target file path using ``file_path()``
        and writes the provided data object to the file in JSON format.
        Existing content will be overwritten."""

        # Take data (players , campaign?) and save

        with open(self.file_path(), "w", encoding="utf-8") as f:
            data = self.json_players() # Change with campaign
            json.dump(data, f,indent=4, ensure_ascii=False)

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

    def json_players(self) -> dict[str, str]:
        """
        Returns a dictionary of players names in JSON format.
        """
        pl_names = {f"player{i+1}": self.players[i].name for i in range(len(self.players))}

        return pl_names

