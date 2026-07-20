from typing import Optional

from battler import Battler

from item import *
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
        self.equipment = {
            # right and left hand are weapons or shields
            "right_hand": None,
            "left_hand": None,
            "helmet": None,
            "boots": None,
            "body": None,
            "legs": None,
            "gloves": None,
            "left_ring": None,
            "right_ring": None,
        }

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



    def equip(self, equipment: Equipment) -> Optional[Equipment]:
        """Equips an item and returns the previously equipped item if one existed."""
        if equipment.slot not in self.equipment:
            print(f"Invalid equipment slot: {equipment.slot}!")
            return None

        # Store the old item to return it to inventory
        old_item = self.equipment[equipment.slot]
        if old_item:
            print(f"Unequipped {old_item.name} from {equipment.slot}")

        # Equip the new item
        self.equipment[equipment.slot] = equipment
        print(f"Equipped {equipment.name} to {equipment.slot}")

        return old_item

    def unequip(self, slot: str) -> Optional[Equipment]:
        """Removes an item from a specific slot and returns it."""
        if slot not in self.equipment:
            print(f"Invalid equipment slot: {slot}!")
            return None

        removed_item = self.equipment[slot]
        if removed_item:
            self.equipment[slot] = None
            print(f"Unequipped {removed_item.name} from {slot}")
            return removed_item

        print(f"Nothing was equipped in {slot}")
        return None

    def _equipment_bonus(self, stat: str) -> int:
        return sum(
            item.bonuses.get(stat, 0)
            for item in self.equipment.values()
            if item is not None
        )

    def _stat(self, name: str) -> int:
        return getattr(self, f"_{name}") + self._equipment_bonus(name)

    @property
    def strength(self):
        return self._stat("strength")

    @property
    def dexterity(self):
        return self._stat("dexterity")

    @property
    def constitution(self):
        return self._stat("constitution")

    @property
    def intelligence(self):
        return self._stat("intelligence")