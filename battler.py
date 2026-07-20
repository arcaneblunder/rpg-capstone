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
        is_defending: bool = False,
    ) -> None:
        self.name = name
        self._hp = hp
        self._maxhp = maxhp
        self._mp = mp
        self._maxmp = maxmp
        self._strength = strength
        self._dexterity = dexterity
        self._constitution = constitution
        self._intelligence = intelligence
        self.is_defending = is_defending
        self.spells = []
        self.statuses = []

    def heal_damage(self, restore_amount: int, over_heal : bool = False) -> int:
        if restore_amount < 0:
            raise ValueError("restore_amount must be non-negative")

        if self.is_alive:
            self._hp += restore_amount

            # check if over heal is True. otherwise, set to the minimum value between hp and maxhp
            if not over_heal:
                self._hp = min(self._hp, self._maxhp)
        return self._hp

    def take_damage(self, damage_amount: int) -> int:
        if damage_amount < 0:
            raise ValueError("damage_amount must be non-negative")

        if self.is_defending:
            damage_amount = damage_amount // 2
            self.is_defending = False

        self._hp = max(0, self.hp - damage_amount)

        if not self.is_alive:
            self.die()

        return damage_amount

    # check if battler is alive
    @property
    def is_alive(self) -> bool:
        return self._hp > 0

    def die(self) -> None:
        print(f"{self.name} has been slain.")

    def spend_mp(self, cost: int) -> bool:
        if self.mp < cost:
            return False

        self.mp -= cost
        return True

    def add_status(self, status):
        existing = next(
            (
                s for s in self.statuses
                if type(s) is type(status)
            ),
            None
        )

        if existing:
            existing.duration = max(
                existing.duration,
                status.duration
            )
            return

        self.statuses.append(status)
        status.on_apply(self)

    def __repr__(self) -> str:
        return (
            f"Battler("
            f"name='{self.name}', "
            f"hp={self.hp}/{self.maxhp}, "
            f"mp={self.mp}/{self.maxmp}"
            f")"
        )

    @property
    def hp(self) -> int:
        return self._hp

    @hp.setter
    def hp(self, value: int) -> None:
        self._hp = value

    @property
    def mp(self) -> int:
        return self._mp

    @mp.setter
    def mp(self, value: int) -> None:
        self._mp = value

    @property
    def maxhp(self) -> int:
        return self._maxhp

    @maxhp.setter
    def maxhp(self, value: int) -> None:
        self._maxhp = value

    @property
    def maxmp(self) -> int:
        return self._maxmp

    @maxmp.setter
    def maxmp(self, value: int) -> None:
        self._maxmp = value

    @property
    def strength(self) -> int:
        return self._strength

    @property
    def dexterity(self) -> int:
        return self._dexterity

    @property
    def constitution(self) -> int:
        return self._constitution

    @property
    def intelligence(self) -> int:
        return self._intelligence