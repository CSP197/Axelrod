"""Tests for the Mindreader strategy."""

import axelrod
from axelrod._strategy_utils import simulate_match
from .test_player import TestPlayer


C, D = axelrod.Action.C, axelrod.Action.D


class TestMindReader(TestPlayer):

    name = "Mind Reader"
    player = axelrod.MindReader
    expected_classifier = {
        'memory_depth': float("inf"),
        'stochastic': False,
        'makes_use_of': set(),
        'long_run_time': False,
        'inspects_source': True,
        'manipulates_source': False,
        'manipulates_state': False
    }

    def test_foil_inspection_strategy(self):
        player = self.player()
        self.assertEqual(player.foil_strategy_inspection(), D)

    def test_strategy(self):
        """
        Will defect against nice strategies
        """
        P1 = axelrod.MindReader()
        P2 = axelrod.Cooperator()
        self.assertEqual(P1.strategy(P2), D)

    def test_vs_defect(self):
        """
        Will defect against pure defecting strategies
        """
        P1 = axelrod.MindReader()
        P2 = axelrod.Defector()
        self.assertEqual(P1.strategy(P2), D)

    def test_vs_grudger(self):
        """
        Will keep nasty strategies happy if it can
        """
        P1 = axelrod.MindReader()
        P2 = axelrod.Grudger()
        self.assertEqual(P1.strategy(P2), C)

    def test_vs_tit_for_tat(self):
        """
        Will keep nasty strategies happy if it can
        """
        P1 = axelrod.MindReader()
        P2 = axelrod.TitForTat()
        self.assertEqual(P1.strategy(P2), C)

    def test_simulate_matches(self):
        """
        Simulates a number of matches
        """
        P1 = axelrod.MindReader()
        P2 = axelrod.Grudger()
        simulate_match(P1, P2, C, 4)
        self.assertEqual(P2.history, [C, C, C, C])

    def test_history_is_same(self):
        """
        Checks that the history is not altered by the player
        """
        P1 = axelrod.MindReader()
        P2 = axelrod.Grudger()
        P1.history = [C, C]
        P2.history = [C, D]
        P1.strategy(P2)
        self.assertEqual(P1.history, [C, C])
        self.assertEqual(P2.history, [C, D])

    def test_vs_geller(self):
        """Ensures that a recursion error does not occur """
        P1 = axelrod.MindReader()
        P2 = axelrod.Geller()
        P1.strategy(P2)
        P2.strategy(P1)

    def test_init(self):
        """Tests for init method """
        P1 = axelrod.MindReader()
        self.assertEqual(P1.history, [])

    def test_reset(self):
        """Tests to see if the class is reset correctly """
        P1 = axelrod.MindReader()
        P1.history = [C, D, D, D]
        P1.reset()
        self.assertEqual(P1.history, [])


class TestProtectedMindReader(TestPlayer):

    name = "Protected Mind Reader"
    player = axelrod.ProtectedMindReader
    expected_classifier = {
        'memory_depth': float("inf"),
        'stochastic': False,
        'makes_use_of': set(),
        'long_run_time': False,
        'inspects_source': True,  # Finds out what opponent will do
        'manipulates_source': True,  # Stops opponent's strategy
        'manipulates_state': False
    }

    def test_foil_inspection_strategy(self):
        player = self.player()
        self.assertEqual(player.foil_strategy_inspection(), D)

    def test_strategy(self):
        """
        Will defect against nice strategies
        """
        P1 = axelrod.ProtectedMindReader()
        P2 = axelrod.Cooperator()
        self.assertEqual(P1.strategy(P2), D)

    def test_vs_defect(self):
        """
        Will defect against pure defecting strategies
        """
        P1 = axelrod.ProtectedMindReader()
        P2 = axelrod.Defector()
        self.assertEqual(P1.strategy(P2), D)

    def tests_protected(self):
        """Ensures that no other player can alter its strategy """

        P1 = axelrod.ProtectedMindReader()
        P2 = axelrod.MindController()
        P3 = axelrod.Cooperator()
        P2.strategy(P1)
        self.assertEqual(P1.strategy(P3), D)


class TestMirrorMindReader(TestPlayer):

    name = 'Mirror Mind Reader'
    player = axelrod.MirrorMindReader
    expected_classifier = {
        'memory_depth': float("inf"),
        'stochastic': False,
        'makes_use_of': set(),
        'long_run_time': False,
        'inspects_source': True, # reading and copying the source of the component
        'manipulates_source': True, # changing own source dynamically
        'manipulates_state': False
    }

    def test_foil_inspection_strategy(self):
        player = self.player()
        self.assertEqual(player.foil_strategy_inspection(), C)

    def test_strategy(self):
        P1 = axelrod.MirrorMindReader()
        P2 = axelrod.Cooperator()
        self.assertEqual(P1.strategy(P2), C)

    def test_vs_defector(self):
        P1 = axelrod.MirrorMindReader()
        P2 = axelrod.Defector()
        self.assertEqual(P1.strategy(P2), D)

    def test_nice_with_itself(self):
        P1 = axelrod.MirrorMindReader()
        P2 = axelrod.MirrorMindReader()
        self.assertEqual(P1.strategy(P2), C)
