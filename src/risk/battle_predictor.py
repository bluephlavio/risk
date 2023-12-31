import numpy as np
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt

from .dice_roll import calc_dice_roll_probabilities

class BattlePredictor:
    def __init__(self, attackers, defenders):
        self._attackers = attackers
        self._defenders = defenders
        self._probabilities = np.zeros((self.attackers + 1, self.defenders + 1))
        self._probabilities[-1, -1] = 1

    @property
    def attackers(self):
        return self._attackers

    @property
    def defenders(self):
        return self._defenders

    @property
    def probabilities(self):
        return self._probabilities

    def _evolve_single_state(self, i, j):
        probabilities = np.zeros((self.attackers + 1, self.defenders + 1))
        if i > 1 and j > 0:
            attack_dice = min(i - 1, 3)
            defence_dice = min(j, 3)
            dice_roll_probs = calc_dice_roll_probabilities(attack_dice, defence_dice)
            for (attack_losses, defence_losses), prob in np.ndenumerate(dice_roll_probs):
                probabilities[i - attack_losses, j - defence_losses] += prob
        else:
            probabilities[i, j] = 1
        return probabilities

    def can_evolve(self):
        for (i, j), probability in np.ndenumerate(self.probabilities):
            if probability > 0 and i > 1 and j > 0:
                return True
        return False

    def evolve(self):
        probabilities = np.zeros((self.attackers + 1, self.defenders + 1))
        for (i, j), probability in np.ndenumerate(self.probabilities):
            probabilities += probability * self._evolve_single_state(i, j)
        self._probabilities = probabilities

    def reset(self):
        self._probabilities = np.zeros((self.attackers + 1, self.defenders + 1))
        self._probabilities[-1, -1] = 1

    def loop(self):
        if self.can_evolve():
            self.evolve()
        else:
            self.reset()

    @property
    def df(self):
        df = pd.DataFrame(self.probabilities)
        df.index.name = 'Attackers'
        df.columns.name = 'Defenders'
        df['Total'] = df.sum(axis=1)
        df.loc['Total'] = df.sum()
        return df

    @property
    def style(self):
        df = self.df
        styled_df = df.style.format('{:.1%}')
        styled_df.set_table_styles([
            {'selector': 'td', 'props': [('min-width', '42px')]},
            {'selector': 'th', 'props': [('font-weight', 'bold')]}
        ])
        cmap_marginal = plt.cm.get_cmap('Reds')
        styled_df.background_gradient(cmap=cmap_marginal, axis=None)
        cmap_main = plt.cm.get_cmap('Blues')
        styled_df.background_gradient(
            cmap=cmap_main,
            subset=pd.IndexSlice[df.index[:-1], df.columns[:-1]],
            axis=None
        )
        return styled_df
