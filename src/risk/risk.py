import random


def roll(n=1):
    faces = [(i + 1) for i in range(6)]
    return sorted([random.choice(faces) for _ in range(n)], reverse=True)


def gains(attack, defence):
    attack = sorted(attack, reverse=True)
    defence = sorted(defence, reverse=True)
    a_gains, d_gains = 0, 0
    for i in range(min(len(attack), len(defence))):
        if attack[i] > defence[i]:
            a_gains += 1
        else:
            d_gains += 1
    return a_gains, d_gains


def losses(attack, defence):
    a_gains, d_gains = gains(attack, defence)
    return d_gains, a_gains


def a_dices(tanks):
    return min(tanks - 1, 3)


def d_dices(tanks):
    return min(tanks, 3)


class NumberOfTanksNotAllowed(Exception):
    pass


class AttackNotAllowed(Exception):
    pass


class Strategy(object):
    def go_on(self, battle):
        return True


class Battle(object):
    def __init__(self, a_tanks, d_tanks):
        self.a_tanks = a_tanks
        self.d_tanks = d_tanks

    @property
    def a_tanks(self):
        return self._a_tanks

    @a_tanks.setter
    def a_tanks(self, value):
        if value > 0:
            self._a_tanks = value
        else:
            raise NumberOfTanksNotAllowed

    @property
    def d_tanks(self):
        return self._d_tanks

    @d_tanks.setter
    def d_tanks(self, value):
        if value > -1:
            self._d_tanks = value
        else:
            raise NumberOfTanksNotAllowed

    def can_go_on(self):
        return self.a_tanks > 1 and self.d_tanks > 0

    def is_a_winner(self):
        return self.d_tanks == 0

    def evolve(self, a_roll, d_roll, verbose=False):
        if self.can_go_on():
            a_losses, d_losses = losses(a_roll, d_roll)
            if verbose:
                print("attack roll: {}".format(a_roll))
                print("defence roll: {}".format(d_roll))
                print(
                    "attack lose {} tank{}".format(
                        a_losses, "" if a_losses == 1 else "s"
                    )
                )
                print(
                    "defence lose {} tank{}".format(
                        d_losses, "" if d_losses == 1 else "s"
                    )
                )
            self.a_tanks -= a_losses
            self.d_tanks -= d_losses
        else:
            raise AttackNotAllowed

    def simulate(self, oneshot=False, strategy=Strategy(), verbose=False):
        if verbose:
            print(self)
        if self.can_go_on() and (
            strategy(self) if callable(strategy) else strategy.go_on(self)
        ):
            a_roll = roll(a_dices(self.a_tanks))
            d_roll = roll(d_dices(self.d_tanks))
            if verbose:
                print("go on!")
            self.evolve(a_roll, d_roll, verbose=verbose)
            if not oneshot:
                self.simulate(oneshot=False, strategy=strategy, verbose=verbose)
        else:
            if verbose:
                if self.is_a_winner():
                    print("attack wins!")
                else:
                    print("defense resists!")

    def __str__(self):
        return "attack tanks: {}, defence tanks: {}".format(self.a_tanks, self.d_tanks)
