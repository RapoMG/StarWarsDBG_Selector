from elements import neutral
from random import randrange, shuffle

class Table:
    """
    Game table class.
    """
    def __init__(self, names):
        self.players = 0
        self.names = names # List of players (Player objects)
        self.factions_pool = []
        self.neut = neutral

    def nbr_of_players(self, val):
        """
        Set number of players.
        """
        self.players = val

    def set_game(self, fcts):
        """
        Set game.
        Returns:
            bool: True if the selection is complete, False otherwise.
        """
        # Get copy of factions to draw from
        self.factions_pool = list(fcts)

        # Bail out early if the selection is incomplete.
        if len(self.factions_pool) < self.players:
            return False

        #Draw factions
        self.draw()

        # Neutral deck "selection"
        self.neutral()

        # Chose draw rules
        if self.players == 2:
            self.players2()
        elif self.players == 3:
            self.players3()
        elif self.players == 4:
            self.players4()

        # Clean fon new selection
        self.factions_pool.clear()
        return True

    def draw(self):
        """
        Draw factions.
        """
        # Probably unnecessary complicated
        # draw factions
        f = 0 # Already drawn factions
        while f < self.players:
            # random player
            rnd = randrange(0, self.players)

            # random faction for the selected players
            # Check if player already have faction
            if self.names[rnd].faction is None:
                rndf = randrange(0, len(self.factions_pool))
                self.names[rnd].add_faction(self.factions_pool.pop(rndf))  # ERR for players equal to no. of factions
                f += 1
            # last player if
            if self.players - f == 1 and len(self.factions_pool) == 1:
                for p in range(self.players):  # find last player
                    if self.names[p].faction is None:  # last player dont have the faction
                        self.names[p].add_faction(self.factions_pool[0])  # last faction for last player
                        f += 1

    def first_player(self):
        """
        Draw first player.
        """
        # A loop used to create teams in a game for 4 players
        while True:
            frst_plr = randrange(0, self.players)
            # Check if the player was selected previously
            if not self.names[frst_plr].first:
                self.names[frst_plr].first = True
                break

    # Set Starter
    def players2(self, pl_pos=[0,1]):
        """**pl_pos** is used to simplify the *players3()* method """
        a = pl_pos[0]
        b = pl_pos[1]

        # Check if its same set
        if self.names[a].faction.box == self.names[b].faction.box:
            # if Yes, check who has starting faction
            if self.names[a].faction.starter:
                self.names[a].first = True
            else:
                self.names[b].first = True
        # Different set: Random 1st player
        else:
            self.first_player()

    def players3(self):
        """
        Set starter for 3 players.
        """
        # If mando and one set, then check for starter
        no_mando = True

        # Mandalorian 1st player rules:
        # Check if Mandalorian faction is in play
        for i in range(self.players):
            if self.names[i].faction.box == "Mandalorian":
                # mark other players
                other = [0,1,2]
                other.remove(i)
                # Check if other factions are from the same set
                # and draw depending on result
                self.players2(other)
                # Turn off no_mando selection
                no_mando = False

        # No Mandalorian faction among selected
        if no_mando:
            self.first_player()

    def players4(self):
        """
        Set starter for 4 players.
        """
        # Select 1st player twice: it's starting team

        # 1st starting player
        self.first_player()

        # 2nd starting player
        self.first_player()

    def neutral(self):
        """
        Random neutral deck as list shuffle, to change if there will be more than two decks.
        """
        shuffle(self.neut)
