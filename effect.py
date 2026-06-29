from status import RegenStatus, StunStatus, WeakStatus, PoisonStatus


class Effect:
    def __init__(self, target_type="selected"):
        self.target_type = target_type
    def apply(self, caster, target, spell, battle):
        raise NotImplementedError

class HealEffect(Effect):
    def __init__(self, target_type="selected"):
        super().__init__(target_type)
    def apply(self, caster, target, spell, battle):
        heal_amount = caster.intelligence * spell.power

        target.hp += heal_amount

        # clamp to max hp
        if target.hp > target.maxhp:
            target.hp = target.maxhp

        print(
            f"{caster.name} heals {target.name} "
            f"for {heal_amount} HP!"
        )

class DamageEffect(Effect):
    def __init__(self, target_type="selected"):
        super().__init__(target_type)

    def apply(self, caster, target, spell, battle):
        damage = caster.intelligence * spell.power

        for status in caster.statuses:
            damage = status.modify_damage_dealt(damage)

        actual_damage = target.take_damage(damage)

        print(
            f"{caster.name} deals {actual_damage} damage to {target.name} "
            f"with {spell.name}!"
        )

# coefficient addition for over time effects?
class RegenEffect(Effect):
    def __init__(self, duration: int = 1, target_type="selected"):
        super().__init__(target_type)
        self.duration = duration

    def apply(self, caster, target, spell, battle):
        heal_amount = int(caster.intelligence * spell.power)

        target.statuses.append(
            RegenStatus(
                heal_amount=heal_amount,
                duration=self.duration
            )
        )

        print(
            f"{target.name} gains regeneration for {self.duration} seconds.!"
        )


class PoisonEffect(Effect):
    def __init__(self, duration: int = 1, target_type="selected"):
        super().__init__(target_type)
        self.duration = duration

    def apply(self, caster, target, spell, battle):
        damage = int(caster.intelligence * spell.power)

        target.statuses.append(
            PoisonStatus(
                damage=damage,
                duration=self.duration
            )
        )
        print(
            f"{target.name} has been poisoned!"
        )

class BurnEffect(Effect):
    def __init__(self, duration: int = 1, target_type="selected"):
        super().__init__(target_type)
        self.duration = duration

    def apply(self, caster, target, spell, battle):
        damage = int(caster.intelligence * spell.power)

        target.statuses.append(
            PoisonStatus(
                damage=damage,
                duration=self.duration
            )
        )
        print(
            f"{target.name} has been set on fire!"
        )

class StunEffect(Effect):
    def __init__(self, duration: int = 1, target_type="selected"):
        super().__init__(target_type)
        self.duration = duration

    def apply(self, caster, target, spell, battle):
        target.add_status(
            StunStatus(duration=self.duration)
        )

        print(f"{target.name} is stunned!")

class WeakEffect(Effect):
    def __init__(self, duration: int = 1, target_type="selected"):
        super().__init__(target_type)
        self.duration = duration

    def apply(self, caster, target, spell, battle):
        target.add_status(
            WeakStatus(duration=self.duration)
        )

        print(f"{target.name} is weakened!")