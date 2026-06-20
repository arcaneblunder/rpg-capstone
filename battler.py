class Battler:
    def __init__(
        self,
        name: str,
        hp: int,
        maxhp: int,
        mp: int,
        maxmp: int,
        strength: int,
        dexterity: int,
        constitution: int,
        intelligence: int,
        is_defending: bool = False
    ) -> None:
        self.name = name
        self.hp = hp
        self.maxhp = maxhp
        self.mp = mp
        self.maxmp = maxmp
        self.strength = strength
        self.dexterity = dexterity
        self.constitution = constitution
        self.intelligence = intelligence
        self.is_defending = is_defending
        self.spells = []

    def heal_damage(self, restore_amount: int, over_heal : bool = False) -> int:
        if restore_amount < 0:
            raise ValueError("restore_amount must be non-negative")

        if self.is_alive:
            self.hp += restore_amount

            # check if over heal is True. otherwise, set to the minimum value between hp and maxhp
            if not over_heal:
                self.hp = min(self.hp, self.maxhp)
        return self.hp

    def take_damage(self, damage_amount: int) -> int:
        if damage_amount < 0:
            raise ValueError("damage_amount must be non-negative")

        if self.is_defending:
            damage_amount = damage_amount // 2
            self.is_defending = False

        self.hp = max(0, self.hp - damage_amount)

        if not self.is_alive:
            self.die()

        return damage_amount

    # check if battler is alive
    @property
    def is_alive(self) -> bool:
        return self.hp > 0

    def die(self) -> None:
        print(f"{self.name} has been slain.")

    def spend_endurance(self) -> None:
        print(f"{self.name} uses skill.")

    def spend_mp(self, cost: int) -> bool:
        if self.mp < cost:
            return False

        self.mp -= cost
        return True

    def __repr__(self) -> str:
        return (
            f"Battler("
            f"name='{self.name}', "
            f"hp={self.hp}/{self.maxhp}, "
            f"mp={self.mp}/{self.maxmp}"
            f")"
        )