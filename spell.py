class Spell:
    def __init__(self, name: str, mp_cost: int, power: float | int, target_type: str, effect):
        self.name = name
        self.mp_cost = mp_cost
        self.power = power
        self.target_type = target_type
        self.effect = effect