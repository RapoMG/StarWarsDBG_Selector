from elements import neutral, players as names
from random import randrange, shuffle

class Table:
    def __init__(self):
        self.players = 0
        self.factions_pool = []
        self.neut = neutral

    def nbr_of_players(self, val):
        self.players = val

    def set_game(self, fcts):
        # Get copy of factions to draw from
        #self.factions_pool.clear() # Clean old selection while draw()
        self.factions_pool = fcts

        #Draw factions
        self.draw()

        # Neutral deck "selection"
        self.neutral()

        # Chose draw rules
        if self.players == 2:
            self.players2()
        if self.players == 3:
            self.players3()
        if self.players == 4:
            self.players4()

        # Clean fon new selection
        self.factions_pool.clear()

    def draw(self):
        # Probably unnecessary complicated
        # draw factions
        f = 0 # Already drawn factions
        while f < self.players:
            # random player
            rnd = randrange(0, self.players)

            # random faction for the selected players
            # Check if player already have faction
            if names[rnd].faction is None:
                rndf = randrange(0, len(self.factions_pool))
                names[rnd].add_faction(self.factions_pool.pop(rndf))  # ERR for players equal to no. of factions
                f += 1
            # last player if
            if self.players - f == 1 and len(self.factions_pool) == 1:
                for p in range(self.players):  # find last player
                    if names[p].faction is None:  # last player dont have the faction
                        names[p].add_faction(self.factions_pool[0])  # last faction for last player
                        f += 1


    def first_player(self):
        # draw first player

        # A loop used to create teams in a game for 4 players
        while True:
            frst_plr = randrange(0, self.players)
            # Check if the player was selected previously
            if not names[frst_plr].first:
                names[frst_plr].first = True
                break


    # Set Starter
    def players2(self, pl_pos=[0,1]):
        """**pl_pos** is used to simplify the *players3()* method """
        a = pl_pos[0]
        b = pl_pos[1]

        # Check if its same set
        if names[a].faction.box == names[b].faction.box:
            # if Yes, check who has starting faction
            if names[a].faction.starter:
                names[a].first = True
            else:
                names[b].first = True
        # Different set: Random 1st player
        else:
            self.first_player()


    def players3(self):
        # If mando and one set, then check for starter
        no_mando = True

        # Mandalorian 1st player rules:
        # Check if Mandalorian faction is in play
        for i in range(self.players):
            if names[i].faction.box == "Mandalorian":
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
        # Select 1st player twice: it's starting team

        # 1st starting player
        self.first_player()

        # 2nd starting player
        self.first_player()

    def neutral(self):
        #random neutral deck as list shuffle, to change if there will be more than two decks
        shuffle(self.neut)