class Table:
    def __init__(self):
        self.players = 0

    def nbr_of_players(self, val):
        self.players = val

    def set_game(self):
        if self.players == 2:
            self.players2()
        if self.players == 3:
            self.players3()
        if self.players == 4:
            self.players4()

    # Set Starter
    def players2(self):
        # If one set check for starter
        # else draw one
        #
        pass

    def players3(self):
        # If mando and one set, then check for starter
        # else draw starter
        pass

    def players4(self):
        # Create teams
        # draw starter team
        pass