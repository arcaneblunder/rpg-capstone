class Status:
    def __init__(self, duration: int):
        self.duration = duration

    @property
    def name(self) -> str:
        return self.__class__.__name__

    def on_apply(self, battler):
        pass

    def on_turn_start(self, battler):
        pass

    def on_turn_end(self, battler):
        pass

    def on_expire(self, battler):
        pass

    def tick(self):
        self.duration -= 1

    @property
    def expired(self) -> bool:
        return self.duration <= 0

    def can_act(self, battler):
        return True

    def modify_damage_dealt(self, value: int) -> int:
        return value


class RegenStatus(Status):
    def __init__(self, heal_amount: int, duration: int):
        super().__init__(duration)
        self.heal_amount = heal_amount

    def on_turn_start(self, battler):
        battler.hp = min(
            battler.maxhp,
            battler.hp + self.heal_amount
        )

        print(
            f"{battler.name} regenerates "
            f"{self.heal_amount} HP."
        )

        self.tick()

class PoisonStatus(Status):
    def __init__(self, damage: int, duration: int):
        super().__init__(duration)
        self.damage = damage

    def on_turn_start(self, battler):
        actual_damage = battler.take_damage(self.damage)

        print(
            f"{battler.name} suffers "
            f"{actual_damage} poison damage."
        )

        self.tick()

class BurnStatus(Status):
    def __init__(self, damage: int, duration: int):
        super().__init__(duration)
        self.damage = damage

    def on_turn_start(self, battler):
        actual_damage = battler.take_damage(self.damage)

        print(
            f"{battler.name} suffers "
            f"{actual_damage} burn damage."
        )

        self.tick()

class StunStatus(Status):
    def __init__(self, duration: int = 1):
        super().__init__(duration)

    def can_act(self, battler):
        return False

    def on_turn_end(self, battler):
        self.tick()

class WeakStatus(Status):
    def __init__(self, duration: int = 1):
        super().__init__(duration)

    def modify_damage_dealt(self, value: int) -> int:
        return int(value * self.multiplier)

    def on_turn_end(self, battler):
        self.tick()