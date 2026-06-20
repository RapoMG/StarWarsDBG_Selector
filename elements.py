from typing import List, Optional


class Faction:
    def __init__(self, name: str, box: str =None, starter=False):
        """Args:\n
         **name** (str) - full name of the faction deck, used by the API\n
         **box** (str) - name of the setting box, used to comparisons by the *Table* class\n
         **starter** (bool) - variable used to mark starting faction from the box"""
        self.name = name
        self.box = box
        self.starter = starter

        self.cards = ["Shuttle", "Trooper", "Guard"]

        self.default_cards = ("Shuttle", "Trooper", "Guard")

    def rename_cards(self, index: int, name: str):
        """
        Renames a card in the faction's cards list.
        If the name is empty, the card is reset to its default name.\n
        Args:\n
            **index** (int): index of the card to be renamed\n
            **name** (str): new name for the card """
        try:
            if name != "":
                self.cards[index] = name
            else:
                self.cards[index] = self.default_cards[index]
        except IndexError:
            print(f"Index {index} is out of range. Max index: {len(self.cards) - 1}")


class Reinforcements:
    """
    Cards added to the deck by Reinforcements Expansion.
    Separate from Faction class to allow usage in different factions. (Unofficial rules)
    """
    def __init__(self, faction_name: str):
        self.faction_name = faction_name
        self.cards = ["Droid", "Raider", "Capital ship", "Fighter 1", "Fighter 2"]
        self.default_cards = ("Droid", "Raider", "Capital ship", "Fighter 1", "Fighter 2")

    def rename_cards(self, index: int, name: str):
        """
        Renames a card in the reinforcement's cards list.
        If the name is empty, the card is reset to its default name.\n
        Args:\n
            **index** (int): index of the card to be renamed\n
            **name** (str): new name for the card """
        try:
            if name != "":
                self.cards[index] = name
            else:
                self.cards[index] = self.default_cards[index]
        except IndexError:
            print(f"Index {index} is out of range. Max index: {len(self.cards) - 1}")



class Player:
    def __init__(self, name: str):
        """
        :param name: player name
        :type name: str
        :var self.faction: Faction class instance assigned to the player by *Table* class
        :type self.faction: object
        :var self.first: value marking player starting the game
        :type self.first: bool
        """
        self.name = name
        self.faction: Optional[Faction] = None
        self.first = False
        self.reinforcements: Optional[Reinforcements] = None

    def add_faction(self, faction: Faction):
        """
        Assigns Faction instance to the player.
        :param faction: Faction class instance
        :type faction: Faction object
        """
        self.faction = faction

    def add_reinforcements(self, rein: Reinforcements):
        """
        Assigns Reinforcements instance to the player.
        :param rein: Reinforcements class instance
        :type rein: Reinforcements object
        """
        self.reinforcements = rein

    def rename(self, name: str):
        self.name = name

class Campaign:
    def __init__(self, players: List[Player], game: int = 1):
        self.players = players
        self.game = game # number of games played in campaign

        self.removed_start: List[str] = []
        self.added_start: List[str] = []

        self.removed_cards: List[str] = []
        self.added_cards: List[str] = []

        self.removed_bases: List[str] = []

        self.even_cards_nbr: bool = True

        # self.expansions = expansions  # expansion used in campaign. Class?
        # TODO:
        #     Create setting to mix faction and expansion decks
        #     Should be here method that checks number of removed cards?
        #     .
        #     Card lists are parts of Reinforcements and Faction
        #     Validation for each group inside respective class
        #     Campaign validates if all are returned True - checked before save or maybe after load?
        #     Number of max card of that type? eg. max 7 shuttles removed?

    @property
    def check_cards_nbr(self) -> bool:
        if len(self.removed_start) != len(self.added_start):
            self.even_cards_nbr = False
        #return len(self.removed_cards) >= len(self.added_cards)
        else:
            self.even_cards_nbr = True

    @staticmethod
    def campaign_valid():
        return True
