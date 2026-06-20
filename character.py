from battler import Battler


class Character(Battler):
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
        level: int = 1,
        experience: int = 0
    ) -> None:
        super().__init__(
            name,
            hp,
            maxhp,
            mp,
            maxmp,
            strength,
            dexterity,
            constitution,
            intelligence,
        )

        self.level = level
        self.experience = experience

    def get_experience(self, exp_gained: int) -> int:
        pass

    def level_up(self) -> None:
        pass

    def cast_spell(self) -> None:
        pass

    def use_skill(self) -> None:
        pass

    def use_item(self, item: str, target: str) -> None:
        pass

    def restore_mp(self, restore_amount: int) -> int:
        if restore_amount < 0:
            raise ValueError("restore_amount must be non-negative")

        if self.is_alive:
            self.mp += restore_amount

            # similar to restore_health in battle.py
            self.mp = min(self.mp, self.maxmp)
        return self.mp

    def spend_mp(self, amount: int) -> bool:
        if amount < 0:
            raise ValueError("amount must be non-negative")

        if self.mp < amount:
            return False

        self.mp -= amount
        return True