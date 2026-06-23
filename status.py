


class RegenStatus:
    def __init__(self, heal_amount, duration):
        self.heal_amount = heal_amount
        self.duration = duration

    def on_turn_start(self, battler):
        battler.hp = min(
            battler.maxhp,
            battler.hp + self.heal_amount
        )

        print(
            f"{battler.name} regenerates "
            f"{self.heal_amount} HP!"
        )

        self.duration -= 1

    @property
    def expired(self):
        return self.duration <= 0