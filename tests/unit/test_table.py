from unittest import TestCase, skip
from unittest.mock import patch
from table import Table
from elements import Faction

class TestTable(TestCase):
    def setUp(self):
        self.tab = Table()

    def test_new_Table(self):
        # Starting values of the Table
        self.assertEqual(self.tab.players, 0, "Initial number of players different than 0")
        self.assertListEqual(self.tab.factions_pool, [], "Starting list should be empty")
        self.assertListEqual(self.tab.neut, ['Core', 'Clone Wars'], "Neutral list is not correct.")

    def test_nbr_of_players(self):
        #New number of players
        self.tab.nbr_of_players(2)

        exp = 2
        msg = f"Number of players is set to {self.tab.players}, while it's expected to be {exp}."

        self.assertEqual(self.tab.players, exp, msg)

    @skip("test not ready")
    def test_set_game(self):
        self.fail()


    @skip("test_draw not ready")
    def test_draw(self):
        self.fail()

    @skip("test_first_player is not ready")
    def test_first_player(self):
        self.fail()

    @skip("test_player2 is not ready")
    def test_players2(self):
        self.fail()

    @skip("test_player3 is not ready")
    def test_players3(self):
        self.fail()

    @skip("test_player4 is an integration test?")
    def test_players4(self):
        self.fail()

    @skip("test_neutral is not ready")
    def test_neutral(self):
        self.fail()

