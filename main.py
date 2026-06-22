from character import Character
from enemy import Enemy
from battle import Battle
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
        name="Damage",
        mp_cost=5,
        power=1.5,
        target_type="enemy",
        effect=DamageEffect()
    )
    heal = Spell(
        name="Heal",
        mp_cost=10,
        power=1.5,
        target_type="ally",
        effect=HealEffect()
    )
    focus = Spell("Focus", 2, 1, "self", "restore_mp")
    hero.spells = [heal]

    mage = Character(
        "Mage", 70, 70, 40, 40,
        8, 10, 8, 15
    )
    mage.spells = [fireball, focus]

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