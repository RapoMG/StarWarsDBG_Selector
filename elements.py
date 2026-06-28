from typing import List, Optional, Dict


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
        self.default_quantity = (7,2,1)

    def rename_card(self, index: int, name: str):
        """
        Renames a card in the faction's cards list.
        If the name is empty, the card is reset to its default name.\n
        Args:\n
            **index** (int): index of the card to be renamed\n
            **name** (str): new name for the card """
        # ToDo: add unique name validator for both factions and reinforcements cards
        #         for card_name in player.reinforcements.cards:
        #             if card_name in player.reinforcements.cards:
        #                 index = player.reinforcements.cards.index(card_name)
        #                 player.reinforcements.rename_card(index, f"{card_name}_r")  # Reset to default if empty
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
        self.cards = ["Droid", "Raider", "Capital ship", "Fighter A", "Fighter B"]
        self.default_cards = ("Droid", "Raider", "Capital ship", "Fighter A", "Fighter B")
        self.max_quantity = (2,2,2,2,2)

    def rename_card(self, index: int, name: str):
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
        self.name: str = name
        self.faction: Optional[Faction] = None
        self.first: bool = False
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
        self.players: list[Player] = players
        self.game: int = game # number of games played in campaign

        # DECKS
        self._p1_start = self._build_start_deck(self.players[0])
        self._p2_start = self._build_start_deck(self.players[1])

        self.p1_removed_cards: Dict[str, int] = {}
        self.p2_removed_cards: Dict[str, int] = {}

        self.p1_added_cards: Dict[str, int] = {}
        self.p2_added_cards: Dict[str, int] = {}

        self.p1_removed_bases: Dict[str, int] = {}
        self.p2_removed_bases: Dict[str, int] = {}

        # VALIDATORS
        self.even_cards_nbr: bool = True

        #add card names validators to classes!
    @staticmethod
    def _build_start_deck(player: Player) -> dict[str, int]:
        """
        Builds a dictionary representing the player's deck with card names as keys and their quantities as values.
        Card names are validated against the player's faction and reinforcements lists.
        If a card name is already used, it is renamed to its default name (with counter if needed).
        :param player: Player class instance
        :return: Dictionary of card names and their quantities
        """
        used = player.faction.cards
        default = player.reinforcements.default_cards

        # Card names validation
        for i, card_name in enumerate(player.reinforcements.cards):
            if card_name not in used:
                used.append(card_name)
                continue

            re_name = default[i]  # get default value

            # Validate if duplicates anyway
            if re_name in used:

                counter = 1
                while f"{re_name}_{counter}" in used:
                    counter += 1
                re_name = f"{re_name}_{counter}"

            player.reinforcements.rename_card(i, re_name)  # Rename to unique name

        # Deck creation
        faction_cards = dict(zip(player.faction.cards, player.faction.default_quantity))
        reinforcements_cards = dict.fromkeys(player.reinforcements.cards, 0)

        return faction_cards | reinforcements_cards

    def players_deck(self, player_nbr: int) -> dict[str, int]:
        """
        Returns the starting deck of the specified player.
        :param player_nbr: Number of the player (1 or 2)
        :return: Dictionary of card names and their quantities
        """
        if 0 < player_nbr <= len(self.players):
            deck =  getattr(self, f"_p{player_nbr}_start")
            return {card: quantity for card, quantity in deck.items() if quantity > 0}
        else:
            raise IndexError("Player number is out of range.")

    def check_starter_nbr(self, player_nbr: int) -> int:
        """
        Checks if the number of cards in the specified player's deck is even 10.
        :param player_nbr: Number of the player (1 or 2)
        :return: Returns ‘True’ if the number of cards is exactly 10;
        otherwise, it returns the difference in the number of cards.
        """
        deck = self.players_deck(player_nbr=player_nbr)
        cards = sum(deck.values())
        #return True if cards == 10 else cards - 10
        return cards - 10

    def check_galaxy_nbr(self, player_nbr: int) -> int:
        """
        Checks if the number of cards in the galaxy deck for each player.
        Number of removed and added cards must be equal.
        :param player_nbr: Number of the player (1 or 2)
        :return: True if the number of cards is even;
        otherwise, it returns the difference in the number of cards.
        """

        removed_deck = getattr(self, f"p{player_nbr}_removed_cards")
        added_deck = getattr(self, f"p{player_nbr}_added_cards")

        removed = sum(removed_deck.values())
        added = sum(added_deck.values())

        #return True if added - removed == 0 else (added - removed)
        return added - removed

    def campaign_valid(self) -> list[tuple[str,str,int]] :
        """
        Checks if the campaign decks have valid sizes.
        Returns the players’ names and the differences between the permitted size and the current size.
        :return: **None** if decks are valid; otherwise, List [("faction name", "starter"|"galaxy", difference)]
        """

        #errors: dict[str, tuple[str, int]] = {}
        errors: list[tuple[str,str,int]] = []

        for p in range(len(self.players)):

            # Starter validation
            starter_val = self.check_starter_nbr(p+1)
            galaxy_val = self.check_galaxy_nbr(p+1)
            if starter_val == 0 and galaxy_val == 0:
                continue

            name = self.players[p].faction.name

            if starter_val != 0:
                errors.append((name, "Starter", starter_val))

            if galaxy_val != 0:
                errors.append((name, "Galaxy", galaxy_val))

        return errors #if len(errors) != 0 else None

    def matching_factions(self) -> bool:
        """
        Validates that the campaign setup follow official rules.
        :return: **True** if both players use matching faction and reinforcements decks; **False** otherwise
        """
        player1_set = True if self.players[0].faction.name == self.players[0].reinforcements.faction_name else False
        player2_set = True if self.players[1].faction.name == self.players[1].reinforcements.faction_name else False

        return True if player1_set and player2_set else False

 # if type(start_val) is int:
            #     if start_val > 0:
            #         return f"{self.players[p].name} has too many starter cards."
            #     else:
            #         return f"{self.players[p].name} doesn't have enough starter cards."
            #
            # # Galaxy deck validation
            # galaxy_val = self.check_galaxy_nbr(p + 1)
            # if type(galaxy_val) is int:
            #     if galaxy_val > 0:
            #         return f"{self.players[p].name} has too many cards in the Galaxy deck."
            #     else:
            #         return f"{self.players[p].name} doesn't have enough cards in the Galaxy deck."