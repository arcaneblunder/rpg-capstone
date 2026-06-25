class Action:
    def execute(self, battle, user):
        raise NotImplementedError

class AttackAction(Action):
    def __init__(self, target):
        self.target = target

    def execute(self, battle, user):
        battle.basic_attack(user, self.target)

class DefendAction(Action):
    def execute(self, battle, user):
        battle.defend(user)

class SpellAction(Action):
    def __init__(self, spell, target):
        self.spell = spell
        self.target = target

    def execute(self, battle, caster):
        if caster.mp < self.spell.mp_cost:
            print(f"{caster.name} does not have enough MP!")
            return

        caster.mp -= self.spell.mp_cost

        for effect in self.spell.effects:

            targets = battle.resolve_targets(
                caster,
                self.target,
                effect.target_type
            )

            for target in targets:
                effect.apply(
                    caster,
                    target,
                    self.spell,
                    battle
                )

class ItemAction(Action):
    def __init__(self, item, target):
        self.item = item
        self.target = target

    def execute(self, battle, user):
        for effect in self.item.effects:

            targets = battle.resolve_targets(
                user,
                self.target,
                effect.target_type
            )

            for target in targets:
                effect.apply(
                    caster=user,
                    target=target,
                    spell=None,
                    battle=battle
                )