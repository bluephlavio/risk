import numpy as np

from .risk import *

DEFAULT_ITER = 1000

def montecarlo(a, d, strategy=Strategy(), iterations=DEFAULT_ITER):
    frequencies = np.zeros(shape=(a+1, d+1))
    for _ in range(iterations):
        battle = Battle(a, d)
        battle.simulate(oneshot=False, strategy=strategy)
        frequencies[battle.a_tanks, battle.d_tanks] += 1
    return frequencies

def p(a, d, strategy=Strategy(), iterations=DEFAULT_ITER):
    frequencies = montecarlo(a, d, strategy, iterations)
    return np.sum(frequencies, 0)[0]/np.sum(frequencies)
