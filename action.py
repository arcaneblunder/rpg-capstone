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

        self.spell.effect.apply(
            caster=caster,
            target=self.target,
            spell=self.spell,
            battle=battle
        )