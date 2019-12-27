from sigmascores import SigmaScore, Card
import numpy as np
import pandas as pd


class ProfitScore:

    def __init__(self, table_cards, my_cards, big_blind=2, n_players=3):
        if len(my_cards) != 2:
            raise ValueError("private cards not defined")
        self.current_cost = 0
        self.table_cards = table_cards
        self.my_cards = my_cards
        self.n_players = n_players
        self.sigma = SigmaScore(table_cards=self.table_cards, my_cards=self.my_cards)()
        self.big_blind = big_blind

        my_money_ref = pd.read_csv("resources/my_money_score.csv", header=None)
        self.my_money_ref_score = my_money_ref.iloc[:, 0].values
        self.my_money_ref_fraction = my_money_ref.iloc[:, 1].values
        adv_money_ref = pd.read_csv("resources/adv_money_score.csv", header=None)
        self.adv_money_ref_score = adv_money_ref.iloc[:, 0].values
        self.adv_money_ref_fraction = adv_money_ref.iloc[:, 1].values

    def __call__(self, pot_total, round_bets, current_cost):

        pot_total += np.sum(round_bets)

        if len(self.table_cards) == 0:
            # what if adversary raised before flop? relevant?
            if self.sigma <= 0:
                return "fold"
            elif self.sigma > 1.0:
                return "raise: sigma = " + str(self.sigma)
            else:
                return "call"

        else:
            if self.sigma <= -1000:
                return "fold"
            else:
                if max(round_bets) == 0:
                    return "check or raise: sigma = " + str(self.sigma)

                adv_money_score = (self.big_blind *self.big_blind) / (max(round_bets) * np.mean(round_bets))
                adv_money_idx = min(list(range(len(self.adv_money_ref_score))), key=lambda i: (self.adv_money_ref_score[i] - adv_money_score) ** 2)

                my_money_score = (current_cost * pot_total) / (max(round_bets) * self.big_blind * self.n_players)
                my_money_idx = min(list(range(len(self.my_money_ref_score))), key=lambda i: (self.my_money_ref_score[i] - my_money_score) ** 2)

                return "\n sigma score = " + str(round(self.sigma, 3)) + "\n adv money fraction = " + str(round(self.adv_money_ref_fraction[adv_money_idx], 3)) \
                       + "\n my money fraction = " + str(round(self.my_money_ref_fraction[my_money_idx], 3)) + "\n"