from status import RegenStatus, StunStatus

class Effect:
    def apply(self, caster, target, spell, battle):
        raise NotImplementedError

class HealEffect(Effect):
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

class DamageEffect:
    def apply(self, caster, target, spell, battle):
        damage = caster.intelligence * spell.power

        actual_damage = target.take_damage(damage)

        print(
            f"{caster.name} deals {actual_damage} damage to {target.name} "
            f"with {spell.name}!"
        )

class RegenEffect:
    def apply(self, caster, target, spell, battle):
        heal_amount = int(caster.intelligence * spell.power)

        target.statuses.append(
            RegenStatus(
                heal_amount=heal_amount,
                duration=3
            )
        )

        print(
            f"{target.name} gains regeneration!"
        )

class StunEffect:
    def __init__(self, duration: int = 1):
        self.duration = duration

    def apply(self, caster, target, spell, battle):
        target.add_status(
            StunStatus(duration=self.duration)
        )

        print(f"{target.name} is stunned!")