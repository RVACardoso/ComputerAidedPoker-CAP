from collections import Counter
import itertools
import matplotlib.pyplot as plt
import numpy as np
import multiprocessing as mp
import pandas as pd


class Card:

    def __init__(self, suit, rank):
        self.__suit = suit
        self.__rank = rank
        if isinstance(self.__rank, int):
            self.__value = self.__rank
        elif self.__rank == 'J' or self.__rank == 'j':
            self.__value = 11
        elif self.__rank == 'Q' or self.__rank == 'q':
            self.__value = 12
        elif self.__rank == 'K' or self.__rank == 'k':
            self.__value = 13
        elif self.__rank == 'A' or self.__rank == 'a':
            self.__value = 14
        else:
            raise ValueError("Card rank must be 2-10, J, Q, K or A.")

    @property
    def suit(self):
        return self.__suit

    @property
    def value(self):
        return self.__value

    @property
    def rank(self):
        return self.__rank

    def __eq__(self, other):
        return self.value == other.value and self.suit == other.suit

    def __repr__(self):
        return str(self.rank) + "  " + str(self.suit)


class PartialDeck:

    def __init__(self, drawn_cards, gen):
        self.drawn_cards = drawn_cards
        self.gen = gen
        self.cards = []

        rank_list = list(range(2, 11)) + ['J', 'Q', 'K', 'A']
        for suit in ["clubs", "diamonds", "hearts", "spades"]:
            for rank in rank_list:
                new_card = Card(suit, rank)
                if new_card not in self.drawn_cards:
                    self.cards.append(new_card)

    def __call__(self):
        if self.gen == 3:
            deck_len = len(self.cards)
            for idx1 in range(deck_len - 1):
                for idx2 in range(idx1 + 1, deck_len):
                    for idx3 in range(idx2 + 1, deck_len):
                        yield [self.cards[idx1], self.cards[idx2], self.cards[idx3]]
        elif self.gen == 2:
            deck_len = len(self.cards)
            for idx1 in range(deck_len-1):
                for idx2 in range(idx1+1, deck_len):
                    yield [self.cards[idx1], self.cards[idx2]]
        elif self.gen == 1:
            for elem in self.cards:
                yield [elem]
        elif self.gen == 0:
            yield None
        else:
            raise ValueError("Partial deck error: gen arg outside correct bounds")


class HandRank:

    # def __init__(self, hands):
    #     self.hand = hands

    @staticmethod
    def _checkconsecutive(l):
        # check if l elements are all consecutive
        return sorted(l) == list(range(min(l), max(l) + 1))

    @staticmethod
    def n_repeated(n, lst):
        # check if lst contains n repeated elements
        return max(Counter(lst).values()) == n

    def handrank(self):

        card_suits, card_values = [], []
        for card in self.hand:
            card_suits.append(card.suit)
            card_values.append(card.value)

        if len(set(card_suits)) == 1:  # some kind of flush
            if self._checkconsecutive(card_values): # royal or straight flush
                if 14 in card_values: # royal flush
                    return 10, "royal flush"
                else:
                    return 9, "straight flush"
            else:
                return 6, "flush"

        else:  # suits are not all equal (no flushes)
            set_len = len(set(card_values))
            if set_len == 5: # no repetitions
                if self._checkconsecutive(card_values):
                    return 5, "straight"
                else:
                    return 1, "high card"
            elif set_len == 4:
                return 2, "pair"
            elif set_len == 3: # 3 of a kind or 2 pairs
                if self.n_repeated(3, card_values):
                    return 4, "3 of a kind"
                else:
                    return 3, "2 pairs"
            elif set_len == 2: # 4 of a kind or full house
                if self.n_repeated(4, card_values):
                    return 8, "4 of a kind"
                else:
                    return 7, "full house"
            else:
                raise ValueError("Incorrect hand given to HandRank")


class HandScore(HandRank):

    def __init__(self, hand_list):
        self.hand_list = hand_list
        # self()

    @staticmethod
    def get_value_idx(value, lst):
        if value in lst:
            indexes = []
            for idx, elem in enumerate(lst):
                if elem == value:
                    indexes.append(idx)
            return indexes
        else:
            return None

    @staticmethod
    def freq_sort(lst):
        counts = Counter(lst)
        return sorted(set(lst), key=lambda x: -counts[x])

    def __call__(self):
        rank_nmr_list = []
        for self.hand in self.hand_list:

            # print(self.handrank())
            rank_nmr, rank = self.handrank()

            if rank_nmr == 9 or rank_nmr == 5 or rank_nmr == 6 or rank_nmr == 1 or rank_nmr == 10:  # highest card in hand
                hand_values = sorted([card.value for card in self.hand], reverse=True)
                score = rank_nmr*10000 + hand_values[0]*100 + hand_values[1]
                rank_nmr_list.append(score)
                # print(score)

            elif rank_nmr == 2 or rank_nmr == 4 or rank_nmr == 7 or rank_nmr == 8:  # highest card in subset (pair, 3, 4 of a kind...)
                freq_list = self.freq_sort([card.value for card in self.hand])
                score = rank_nmr * 10000 + freq_list[0] * 100 + max(freq_list[1:])
                rank_nmr_list.append(score)
                # print(score)

            elif rank_nmr == 3:
                freq_list = self.freq_sort([card.value for card in self.hand])
                score = rank_nmr * 10000 + freq_list[0] * 100 + freq_list[1] + freq_list[2]*0.01
                rank_nmr_list.append(score)
                # print(score)
            else:
                print("Rank nmr: ", rank_nmr)
                raise ValueError("ERROR HandScore: rank_nmr out outside expected bounds")

        return rank_nmr_list


class SigmaScore:

    def __init__(self, table_cards, my_cards):
        self.table_cards = table_cards
        self.my_cards = my_cards
        self.adv_pd = PartialDeck(drawn_cards=self.table_cards + self.my_cards, gen=2)
        self.my_hist = []
        self.adv_hist = []
        self.my_edges, self.adv_edges = [], []

        self.c = 0

    def private_calc(self, adv_cards):
        score_list = []
        private_pd = PartialDeck(drawn_cards=self.table_cards+adv_cards+self.my_cards, gen=5-len(self.table_cards))
        for deck_cards in private_pd():  # all possibilities for missing cards

            if len(adv_cards) == 0:
                if deck_cards is None:
                    card_set = self.table_cards + self.my_cards
                else:
                    card_set = self.table_cards + self.my_cards + deck_cards
            else:
                if deck_cards is None:
                    card_set = self.table_cards + adv_cards
                else:
                    card_set = self.table_cards + adv_cards + deck_cards
            assert len(card_set) == 7

            possible_hands = []
            for hand in itertools.combinations(card_set, 5):  # find best hand for each possibility
                possible_hands.append(hand)

            score_list.append(max(HandScore(possible_hands)()))

        return score_list

    def eval_my_cards(self):
        my_scores = self.private_calc(adv_cards=[])
        hist, self.my_edges = np.histogram(my_scores, bins=500, range=(0, 110000))
        self.my_hist = hist/sum(hist)
        return sum(self.my_hist * self.my_edges[:-1])

    def eval_adv_func(self, adv_cards):
        indiv_scores = self.private_calc(adv_cards=adv_cards)
        return indiv_scores

    def eval_adv_cards(self):
        adv_scores = []
        indiv_evals = []

        pool = mp.Pool(mp.cpu_count())
        all_scores = pool.map(self.eval_adv_func, [adv_cards for adv_cards in self.adv_pd()])
        pool.close()

        for indiv_scores in all_scores:
            indiv_hist, indiv_edge = np.histogram(indiv_scores, bins=500, range=(0, 110000))
            indiv_hist = indiv_hist / sum(indiv_hist)
            indiv_evals.append(sum(indiv_hist * indiv_edge[:-1]))
            adv_scores.extend(indiv_scores)

        hist, self.adv_edges = np.histogram(adv_scores, bins=500, range=(0, 110000))
        self.adv_hist = hist/sum(hist)
        return sum(self.adv_hist * self.adv_edges[:-1]), np.std(np.array(indiv_evals))

    def show_odds(self):
        plt.figure()
        plt.plot(self.my_edges[:-1], self.my_hist, color='red', label="Me")
        plt.plot(self.adv_edges[:-1], self.adv_hist, color='blue', label="Avg adv")
        plt.legend()
        plt.show()

    def __call__(self):
        if len(self.table_cards) == 0:
            m1 = self.my_cards[0].suit[0] + str(self.my_cards[0].rank)
            m2 = self.my_cards[1].suit[0] + str(self.my_cards[1].rank)
            preflop_table = pd.read_csv("resources/preflop_table.csv", names=["card1", "card2", "equity_avg", "equity_std"])
            pair_equity = preflop_table.loc[(preflop_table["card1"] == m1) & (preflop_table["card2"] == m2) | (preflop_table["card2"] == m1) & (preflop_table["card1"] == m2)]["equity_avg"]
            # print(pair_equity)

            sigma = (pair_equity.values[0] - 16699.046698432976) / 262.03557734030005
            # print("#sigma: ", sigma)
            return sigma
        else:
            # time1 = time.time()
            my_eval = self.eval_my_cards()
            avg_eval, avg_std = self.eval_adv_cards()
            sigma = (my_eval - avg_eval) / avg_std

            # print("My eval: ", my_eval)
            # print("Avg adv eval: ", avg_eval, " +/- ", avg_std)
            # print("#sigma: ", (my_eval - avg_eval) / avg_std)
            # print("Time (s): ", time.time() - time1)
            # self.show_odds()
            return sigma

