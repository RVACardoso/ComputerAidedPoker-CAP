from pokerlib import PartialDeck, HandScore, Card
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd


class FullDeck:

    def __init__(self):
        self.cards = []

        rank_list = list(range(2, 11)) + ['J', 'Q', 'K', 'A']
        for suit in ["clubs", "diamonds", "hearts", "spades"]:
            for rank in rank_list:
                new_card = Card(suit, rank)
                self.cards.append(new_card)

    def __call__(self):
        deck_len = len(self.cards)
        for idx1 in range(deck_len-1):
            for idx2 in range(idx1+1, deck_len):
                yield [self.cards[idx1], self.cards[idx2]]


class PreFlopScore:

    def __init__(self, card_pair):
        self.card_pair = card_pair
        self.private_pd = PartialDeck(drawn_cards=self.card_pair, gen=3)
        self.score_list = []

    def pair_calc(self):
        private_pd = PartialDeck(drawn_cards=self.card_pair, gen=3)
        for deck_cards in private_pd():  # all possibilities for missing cards

            card_set = self.card_pair + deck_cards
            assert len(card_set) == 5

            score = HandScore([card_set])()
            # try:
            self.score_list.append(*score)
            # except:
            #     print(card_set)
            #     print(score)
            #     print()

    def get_score_list(self):
        self.pair_calc()
        return np.array(self.score_list)

    def eval_pair(self):
        score_list = self.get_score_list()
        # plt.hist(score_list, range=(0, 110000), bins=500)
        # plt.show()
        return np.mean(score_list), np.std(score_list)


def save_preflop_table(file_name):
    fd1 = FullDeck()
    i = 0
    for pair in fd1():
        print(i, "/1326")
        i+=1

        file1 = open(file_name, 'a')
        pfs1 = PreFlopScore(card_pair=pair)
        pair_avg, pair_std = pfs1.eval_pair()
        print(pair[0].suit[0] + str(pair[0].rank), ",", pair[1].suit[0] + str(pair[1].rank), ",", pair_avg, ",", pair_std, file=file1)
        file1.close()


def check_pair(pair):
    pfs1 = PreFlopScore(card_pair=pair)
    plt.hist(pfs1.get_score_list(), range=(0, 110000), bins=500)
    pair_avg, pair_std = pfs1.eval_pair()
    print(pair[0].suit[0] + str(pair[0].rank), ",", pair[1].suit[0] + str(pair[1].rank), ",", pair_avg, ",", pair_std)
    plt.show()

# # Create results
# save_preflop_table("file1.test")

# # Check table results
# preflop_table = pd.read_csv("preflop_table.csv")
#
# equity_avg = preflop_table.iloc[:, 2].values
#
# low_equities = equity_avg[np.where(equity_avg<24000)]
#
# low_equities_avg = np.mean(low_equities)
# low_equities_std = np.std(low_equities)
#
# # print(low_equities_avg)
# # print(low_equities_std)
#
# sigmas = (equity_avg-low_equities_avg)/low_equities_std
#
# plt.figure()
# plt.scatter(list(range(len(sigmas))), sigmas)
# plt.show()

# # check specific pair
# c1 = Card("diamonds", 'A')
# c2 = Card("diamonds", 'K')
# check_pair(pair=[c1, c2])

