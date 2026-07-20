class Item:
    def __init__(self, name, description):
        self.name = name
        self.description = description

class Consumable(Item):
    def __init__(self, name, description, effects, is_consumable=True):
        super().__init__(name, description)
        self.effects = effects or []
        self.is_consumable = is_consumable

    def execute(self, battle, user):
        for effect in self.effects:

            targets = battle.resolve_targets(
                user,
                effect.target,
                effect.target_type
            )

            for target in targets:
                effect.apply(
                    caster=user,
                    target=target,
                    spell=None,
                    battle=battle
                )

class Equipment(Item):
    def __init__(self, name, description, slots, bonuses=None):
        super().__init__(name, description)
        self.slots = slots
        self.bonuses = bonuses or {}