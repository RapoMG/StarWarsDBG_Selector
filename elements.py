class Faction:
    def __init__(self, name: str, box: str =None, starter=False):
        """Args:\n
         **name** (str) - full name of the faction deck, used by the API\n
         **box** (str) - name of the setting box, used to comparisons by the *Table* class\n
         **starter** (bool) - variable used to mark starting faction from the box"""
        self.name = name
        self.box = box
        self.starter = starter


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
        self.faction = None
        self.first = False

    def add_faction(self, faction: object):
        """
        Assigns Faction instance to the player.
        :param faction: Faction class instance
        :type faction: object
        """
        self.faction = faction


# Add setup factions
factions = [
    # Core box
    Faction("Rebels", "Core"),
    Faction("Empire","Core",True),

    # Clone Wars box
    Faction("Republic", "Clone Wars"),
    Faction("Separatists","Clone Wars",True),

    # Mandalorian Expansion
    Faction("Mandalorian","Mandalorian"),
]

# Neutral decks
neutral = [
    factions[0].box,
    factions[2].box,
]

# Default players
players = [
    Player("Player 1"),
    Player("Player 2"),
    Player("Player 3"),
    Player("Player 4"),
]
