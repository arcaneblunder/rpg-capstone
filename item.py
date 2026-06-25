class Item:
    def __init__(self, name, description, effects, item_type: str="consumable", strength_bonus = 0, intelligence_bonus: int = 0):
        self.name = name
        self.description = description
        self.effects = effects or []
        self.item_type = item_type

        self.strength_bonus = strength_bonus
        self.intelligence_bonus = intelligence_bonus

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