
from spell import Spell
from effect import *

def main():
    from battler import Battler
    from character import Character
    from battle import Battle

    hero = Character(
        "Hero", 100, 100, 20, 20,
        15, 10, 10, 8
    )
    fireball = Spell(
        name="Fireball",
        mp_cost=115,
        power=1.5,
        target_type="enemy",
        effects=[DamageEffect(target_type="selected")]
    )
    regen = Spell(
        name="Regen",
        mp_cost=8,
        power=0.5,
        target_type="ally",
        effects=[RegenEffect(target_type="selected")]
    )
    heal = Spell(
        name="Heal",
        mp_cost=1110,
        power=1.5,
        target_type="ally",
        effects=[HealEffect(target_type="selected")]
    )
    focus = Spell(
        name="Focus",
        mp_cost=1,
        power= 1,
        target_type="self",
        effects=[HealEffect(target_type="selected")]
    )
    thunder_shock = Spell(
        name="Thunder Shock",
        mp_cost=8,
        power=0,
        target_type="enemy",
        effects=[StunEffect(
            duration=2,
            target_type="selected"
        )]
    )
    poison = Spell(
        name="Poison",
        mp_cost=1,
        power=1,
        target_type="enemy",
        effects=[PoisonEffect(
            duration=2,
            target_type="selected")]
    )
    big_heal = Spell(
        name="Test",
        mp_cost=1,
        power=1,
        target_type="ally",
        effects=[HealEffect(target_type="selected"), RegenEffect(target_type="selected"), DamageEffect(target_type="all_enemies")]
    )
    hero.spells = [heal, regen, big_heal]

    mage = Character(
        "Mage", 70, 70, 40, 40,
        8, 10, 8, 15
    )
    mage.spells = [fireball, focus, thunder_shock, poison]

    slime = Battler(
        "Slime", 30, 30, 0, 0,
        5, 3, 5, 1
    )

    goblin = Battler(
        "Goblin", 50, 50, 0, 0,
        10, 12, 8, 5
    )

    battle = Battle(
        party=[hero, mage],
        enemies=[slime, goblin]
    )

    battle.start()

if __name__ == "__main__":
    main()