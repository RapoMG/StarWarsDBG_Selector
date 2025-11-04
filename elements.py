class Faction:
    def __init__(self, name, box=None, starter=False):
        self.name = name
        self.box = box
        self.starter = starter

class Player:
    def __init__(self, name):
        self.name = name
        self.faction = None
        self.first = False

    def add_faction(self, faction):
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
