import functools
import itertools

import numpy as np


@functools.lru_cache(maxsize=None)
def calc_dice_roll_probabilities(attack_dice, defence_dice):
    active_tanks = min(attack_dice, defence_dice)
    probabilities = np.zeros((active_tanks + 1, active_tanks + 1))
    for attack_combination in itertools.product([1, 2, 3, 4, 5, 6], repeat=attack_dice):
        attack_combination = sorted(attack_combination, reverse=True)
        for defence_combination in itertools.product([1, 2, 3, 4, 5, 6], repeat=defence_dice):
            defence_combination = sorted(defence_combination, reverse=True)
            defence_losses = 0
            for i in range(active_tanks):
                if attack_combination[i] > defence_combination[i]:
                    defence_losses += 1
            attack_losses = active_tanks - defence_losses
            probabilities[attack_losses, defence_losses] += 1 / 6 ** (attack_dice + defence_dice)
    return probabilities
