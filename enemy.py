from battler import Battler


class Enemy(Battler):
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
        exp_reward: int,
        gold_reward: int,
    ):
        super().__init__(
            name,
            hp,
            maxhp,
            mp,
            maxmp,
            strength,
            dexterity,
            constitution,
            intelligence
        )
        self.exp_reward = exp_reward
        self.gold_reward = gold_reward