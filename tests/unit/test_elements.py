from unittest import TestCase
from elements import Faction, Player


class TestElements(TestCase):
    def test_faction_basic(self):
        f = Faction("Faction name")
        exp = 'Faction name'

        self.assertEqual(exp, f.name, f"Result should be {exp}, but it's {f.name} instead")
        self.assertIsNone(f.box,f"Result should be None, but it's {f.box} instead")
        self.assertFalse(f.starter, f"Result should be False, but it's {f.starter} instead")

    def test_faction_full(self):
        f = Faction("Faction name", "Box name", True)
        exp_n = 'Faction name'
        exp_b = "Box name"

        self.assertEqual(exp_n, f.name, f"Result should be {exp_n}, but it's {f.name} instead")
        self.assertEqual(exp_b, f.box, f"Result should be {exp_b}, but it's {f.box} instead")
        self.assertTrue(f.starter, f"Result should be True, but it's {f.starter} instead")

    def test_player(self):
        p = Player("Player")
        exp = "Player"

        self.assertEqual(exp, p.name, f"Result should be {exp}, but it's {p.name} instead")
        self.assertIsNone(p.faction, f"Result should be None, but it's {p.faction} instead")
        self.assertFalse(p.first,f"Result should be False, but it's {p.first} instead")
