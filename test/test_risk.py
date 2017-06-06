import sys
sys.path.append('../')

import unittest
from risk.risk import *

class TestRisk(unittest.TestCase):

    def setUp(self):
        self.battle = Battle(21,18)

    def test_gains(self):
        self.assertEqual(gains([3,2,1], [5,1]), (1,1))
        self.assertEqual(gains([6,6,6], [6,6,6]), (0,3))
        self.assertEqual(gains([1,1,1], [1]), (0,1))

    def test_losses(self):
        self.assertEqual(losses([3,2,1], [5,1]), (1,1))
        self.assertEqual(losses([6,6,6], [6,6,6]), (3,0))
        self.assertEqual(losses([1,1,1], [1]), (1,0))

    def test_a_dices(self):
        self.assertEqual(a_dices(1), 0)
        self.assertEqual(a_dices(2), 1)
        self.assertEqual(a_dices(3), 2)
        self.assertEqual(a_dices(4), 3)
        self.assertEqual(a_dices(5), 3)

    def test_d_dices(self):
        self.assertEqual(d_dices(1), 1)
        self.assertEqual(d_dices(2), 2)
        self.assertEqual(d_dices(3), 3)
        self.assertEqual(d_dices(4), 3)
        self.assertEqual(d_dices(5), 3)

    def test_battle_simulation(self):
        self.battle.simulate(oneshot=False)
        self.assertFalse(self.battle.can_go_on())

    def test_battle_strategy(self):
        class MyStrategy(Strategy):
            def go_on(self, battle):
                return battle.a_tanks > 21

        strategy = MyStrategy()
        self.battle.simulate(oneshot=False, strategy=strategy)
        self.assertFalse(strategy.go_on(self.battle))
        self.assertTrue(self.battle.a_tanks, 21)
        self.assertFalse(self.battle.is_a_winner())




