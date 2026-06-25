import random
from action import *

class Battle:
    def __init__(self, party, enemies):
        self.party = party
        self.enemies = enemies

    # -------------------------
    # State checks
    # -------------------------
    def party_alive(self) -> bool:
        return any(member.is_alive for member in self.party)

    def enemies_alive(self) -> bool:
        return any(enemy.is_alive for enemy in self.enemies)

    def is_over(self) -> bool:
        return not self.party_alive() or not self.enemies_alive()

    # -------------------------
    # Turn order
    # -------------------------
    def get_turn_order(self):
        battlers = self.party + self.enemies

        return sorted(
            [b for b in battlers if b.is_alive],
            key=lambda b: b.dexterity,
            reverse=True
        )

    # -------------------------
    # Target selection
    # -------------------------
    def get_alive_party(self):
        return [b for b in self.party if b.is_alive]

    def get_alive_enemies(self):
        return [b for b in self.enemies if b.is_alive]

    def choose_enemy_target(self):
        return random.choice(self.get_alive_party())

    def choose_party_target(self):
        alive_enemies = self.get_alive_enemies()

        print("\nChoose a target:")

        for i, enemy in enumerate(alive_enemies, start=1):
            print(f"{i}. {enemy.name} (HP: {enemy.hp}/{enemy.maxhp})")

        while True:
            choice = input("> ")

            if not choice.isdigit():
                print("Enter a number.")
                continue

            index = int(choice) - 1

            if 0 <= index < len(alive_enemies):
                return alive_enemies[index]

    # -------------------------
    # Combat actions
    # -------------------------
    def basic_attack(self, attacker, target):
        damage = attacker.strength
        actual_damage = target.take_damage(damage)
        print(f"{attacker.name} attacks {target.name} for {actual_damage} damage!")

        if not target.is_alive:
            print(f"{target.name} has been defeated!")

    def choose_spell(self, battler):
        print("\nChoose a spell:")

        for i, spell in enumerate(battler.spells, start=1):
            print(f"{i}. {spell.name} (MP: {spell.mp_cost})")

        while True:
            choice = input("> ")

            if choice.isdigit():
                index = int(choice) - 1

                if 0 <= index < len(battler.spells):
                    return battler.spells[index]

            print("Invalid choice.")

    def cast_spell(self, caster, spell, target):
        spell.cast(caster, target)

    def defend(self, battler):
        battler.is_defending = True
        print(f"{battler.name} is defending!")

    # -------------------------
    # Turn processing
    # -------------------------
    def process_turn(self, battler):
        if not battler.is_alive:
            return

        self.process_turn_start_statuses(battler)

        if not battler.is_alive:
            return

        if not self.can_act(battler):
            print(
                f"{battler.name} is unable to act!"
            )

            self.process_turn_end_statuses(battler)
            return

        # -------------------------
        # PLAYER TURN
        # -------------------------
        if battler in self.party:

            action = self.get_player_action(battler)
            action.execute(self, battler)

        # -------------------------
        # ENEMY TURN
        # -------------------------
        else:
            action = AttackAction(self.choose_enemy_target())
            action.execute(self, battler)

            # for ai stuff action = battler.ai_choose_action(self)

    # -------------------------
    # Main loop
    # -------------------------
    def start(self):
        print("=== BATTLE START ===")

        while not self.is_over():

            turn_order = self.get_turn_order()

            for battler in turn_order:

                if self.is_over():
                    break

                self.process_turn(battler)

        print("\n=== BATTLE RESULT ===")

        if self.party_alive():
            print("Victory!")
        else:
            print("Defeat!")


    def player_choose_action(self, battler) -> str:
        print(f"\n{battler.name}'s turn: HP: {battler.hp}/{battler.maxhp} MP {battler.mp}/{battler.maxmp}")
        print("1. Attack")
        print("2. Use Spell")
        print("3. Defend")

        choice = input("> ")

        return choice

    def get_allies(self, battler):
        if battler in self.party:
            return self.get_alive_party()
        return self.get_alive_enemies()


    def get_enemies(self, battler):
        if battler in self.party:
            return self.get_alive_enemies()
        return self.get_alive_party()


    def get_targets_for_type(self, battler, target_type):
        allies = self.get_allies(battler)
        enemies = self.get_enemies(battler)

        if target_type == "self":
            return [battler]

        elif target_type == "ally":
            return allies

        elif target_type == "enemy":
            return enemies

        elif target_type == "any":
            return allies + enemies + [battler]


        return []

    def choose_target(self, targets):
        print("\nChoose a target:")

        for i, target in enumerate(targets, start=1):
            print(f"{i}. {target.name} (HP: {target.hp}/{target.maxhp})")

        while True:
            choice = input("> ")

            if choice.isdigit():
                index = int(choice) - 1

                if 0 <= index < len(targets):
                    return targets[index]

            print("Invalid choice.")

    def get_player_action(self, battler):
        print(f"\n{battler.name}'s turn : HP {battler.hp}/{battler.maxhp} | MP {battler.mp}/{battler.maxmp}")

        print("1. Attack")
        print("2. Use Spell")
        print("3. Defend")

        choice = input("> ")

        if choice == "1":
            target = self.choose_party_target()
            return AttackAction(target)

        elif choice == "2":
            spell = self.choose_spell(battler)

            if spell.target_type == "self":
                target = battler
            else:
                target = self.choose_target(
                    self.get_targets_for_type(
                        battler,
                        spell.target_type
                    )
                )

            return SpellAction(spell, target)

        elif choice == "3":
            return DefendAction()

        return AttackAction(self.choose_party_target())

    def process_turn_start_statuses(self, battler):
        for status in battler.statuses[:]:
            status.on_turn_start(battler)

            if status.expired:
                status.on_expire(battler)
                battler.statuses.remove(status)

    def process_turn_end_statuses(self, battler):
        for status in battler.statuses[:]:
            status.on_turn_end(battler)

            if status.expired:
                status.on_expire(battler)
                battler.statuses.remove(status)

    def can_act(self, battler):
        return all(
            status.can_act(battler)
            for status in battler.statuses
        )

    def resolve_targets(
            self,
            caster,
            selected_target,
            target_type
    ):
        if target_type == "selected":
            return [selected_target]

        if target_type == "self":
            return [caster]

        if target_type == "all_allies":
            return self.get_allies(caster)

        if target_type == "all_enemies":
            return self.get_enemies(caster)