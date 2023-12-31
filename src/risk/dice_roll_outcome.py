class DiceRollOutcome:
    def __init__(self, attack_losses, defence_losses):
        self._attack_losses = attack_losses
        self._defence_losses = defence_losses

    @property
    def attack_losses(self):
        return self._attack_losses

    @property
    def defence_losses(self):
        return self._defence_losses

    def __repr__(self):
        return f"Attack losses: {self._attack_losses}, Defence losses: {self._defence_losses}"
