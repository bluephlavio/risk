import sys
sys.path.append('../')

import random, unittest
import numpy as np
from risk.risk import *
from risk.stats import *

DEFAULT_ITERATIONS = 100

class TestStats(unittest.TestCase):

    def setUp(self):
        pass

    def test_montecarlo(self):
        f = montecarlo(10,10, iterations=DEFAULT_ITERATIONS)
        self.assertEqual(np.sum(f), DEFAULT_ITERATIONS)

    def test_p(self):
        n_tests = 10
        min_tanks = 1
        max_tanks = 10
        iterations = DEFAULT_ITERATIONS
        for _ in range(n_tests):
            i = random.randint(min_tanks, max_tanks)
            j = random.randint(min_tanks, max_tanks)
            pij = p(i, j, iterations=iterations)
            pji = p(j, i, iterations=iterations)
            self.assertTrue(pij >= 0 and pij <= 1)
            if i > j:
                self.assertTrue(pij > pji)
            elif i < j:
                self.assertTrue(pij < pji)
            else:
                pass
