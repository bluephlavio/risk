import numpy as np

from .dice_roll import calc_dice_roll_probabilities


class Battle:
    def __init__(self, attackers, defenders):
        self._attackers = attackers
        self._defenders = defenders
        self._probabilities = [np.zeros((attackers + 1, defenders + 1))]
        self._probabilities[0][-1, -1] = 1

    @property
    def attackers(self):
        return self._attackers

    @property
    def defenders(self):
        return self._defenders

    @property
    def probabilities(self):
        return self._probabilities

    def evolve_probabilities(self):
        probabilities = self._probabilities[-1]
        new_probabilities = np.zeros((self._attackers + 1, self._defenders + 1))
        for attack_losses in range(self._attackers + 1):
            for defence_losses in range(self._defenders + 1):
                for attack_dice in range(1, min(attack_losses + 1, 3) + 1):
                    for defence_dice in range(1, min(defence_losses + 1, 2) + 1):
                        new_probabilities[attack_losses, defence_losses] += probabilities[
                            attack_losses - attack_dice, defence_losses - defence_dice
                        ] * calc_dice_roll_probabilities(attack_dice, defence_dice)[attack_dice - 1, defence_dice - 1]
        self._probabilities.append(new_probabilities)

def evolve_battle(attackers, defenders):
    attack_dice = min(attackers - 1, 3)
    defence_dice = min(defenders, 3)
    probabilities = np.zeros((attackers + 1, defenders + 1))
    dice_roll_outcome_probabilities = calc_dice_roll_probabilities(attack_dice, defence_dice)
    for (attack_losses, defence_losses), probability in np.ndenumerate(dice_roll_outcome_probabilities):
        probabilities[attackers - attack_losses, defenders - defence_losses] += probability
    return probabilities    


def predict_battle_outcome(attackers, defenders):
    probabilities = [np.zeros((attackers + 1, defenders + 1))]
    probabilities[0][-1, -1] = 1
    while np.all(probabilities[-1][2:, 1:] == 0):
        non_zero_indices = np.nonzero(probabilities[-1])
        for i, j in zip(*non_zero_indices):
            probability = probabilities[-1][i, j]
            attack_dice = min(i - 1, 3)
            defence_dice = min(j, 3)
            active_tanks = min(attack_dice, defence_dice)
            for attack_losses in range(active_tanks + 1):
                defence_losses = active_tanks - attack_losses

        for attack_losses in range(attackers + 1):
            for defence_losses in range(defenders + 1):
                for attack_dice in range(1, min(attack_losses + 1, 3) + 1):
                    for defence_dice in range(1, min(defence_losses + 1, 2) + 1):
                        probabilities[-1][attack_losses, defence_losses] += probabilities[-2][
                            attack_losses - attack_dice, defence_losses - defence_dice
                        ] * calc_dice_roll_probabilities(attack_dice, defence_dice)[attack_dice - 1, defence_dice - 1]
        probabilities.append(np.zeros((attackers + 1, defenders + 1)))
    return probabilities