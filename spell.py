
class Spell:
    def __init__(self, name: str, mp_cost: int, power: float | int, target_type: str, effect_type: str) -> None:
        self.name = name
        self.mp_cost = mp_cost
        self.power = power
        self.target_type = target_type
        self.effect_type = effect_type

    def cast(self, caster, target):
        if caster.mp < self.mp_cost:
            print(f"{caster.name} does not have enough MP!")
            return False

        caster.mp -= self.mp_cost

        damage = caster.intelligence * self.power
        actual_damage = target.take_damage(damage)

        print(
            f"{caster.name} casts {self.name} on {target.name} "
            f"for {actual_damage} damage!"
        )

        return True