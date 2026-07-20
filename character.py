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

    @property
    def strength(self) -> int:
        """Overrides the raw strength attribute to dynamically include equipment bonuses."""
        bonus_strength = 0

        # Safely pull values whether equipment is a dict or an array
        items_to_check = (
            self.equipment.values()
            if isinstance(self.equipment, dict)
            else self.equipment
        )

        for item in items_to_check:
            if item and hasattr(item, 'bonuses') and isinstance(item.bonuses, dict):
                bonus_strength += item.bonuses.get("strength", 0)

        # Look up the original base value assigned during __init__
        base_strength = self.__dict__.get('_base_strength', None)
        if base_strength is None:
            # Fallback to store it the first time this property runs
            base_strength = self.__dict__.get('strength', 0)
            self.__dict__['_base_strength'] = base_strength

        return base_strength + bonus_strength

    @strength.setter
    def strength(self, value: int) -> None:
        """Allows direct modification of base strength (like during level ups)."""
        self.__dict__['_base_strength'] = value
        self.__dict__['strength'] = value
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