import random
from collections import Counter
import itertools
import matplotlib.pyplot as plt
import numpy as np
import time
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


class Deck:

    def __init__(self):
        self.__cards = []
        rank_list = list(range(2, 11)) + ['J', 'Q', 'K', 'A']
        for suit in ["clubs", "diamonds", "hearts", "spades"]:
            for rank in rank_list:
                self.__cards.append(Card(suit, rank))
        random.shuffle(self.__cards)

    def __call__(self):
        idx = random.randint(0, len(self.__cards) - 1)
        card = self.__cards[idx]
        del self.__cards[idx]
        return card

    def __repr__(self):
        out = ""
        for card in self.__cards:
            out += str(card.rank) + "  " + str(card.suit) + "\n"
        return out


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




# c1 = Card("clubs", 'a')
# c2 = Card("spades", 8)
# c3 = Card("spades", 4)
# c4 = Card("hearts", 'q')
# c5 = Card("diamonds", 8)
# hand1 = [c1, c2, c3, c4, c5]
# pd1 = PartialDeck(drawn_cards=hand1)


class Player:

    def __init__(self, name, balance):
        self.__name = name
        self.__balance = balance
        self.__hand = None

    @property
    def name(self):
        return self.__name

    @property
    def balance(self):
        return self.__balance

    @balance.setter
    def balance(self, value):
        self.__balance = value

    @property
    def hand(self):
        return self.__hand

    def get_hand(self, deck):
        self.__hand = [deck(), deck()]

    def place_bet(self, drawn_cards, max_bet):
        bet_value = 10
        self.balance -= bet_value
        return bet_value

    def __repr__(self):
        return str(self.name) + "   " + str(self.balance)


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


# class BestHand(HandRank):
#
#     def __init__(self, hand_list):
#         self.hand_list = hand_list
#         # self()
#
#     @staticmethod
#     def get_value_idx(value, lst):
#         if value in lst:
#             indexes = []
#             for idx, elem in enumerate(lst):
#                 if elem == value:
#                     indexes.append(idx)
#             return indexes
#         else:
#             return None
#
#     @staticmethod
#     def freq_sort(lst):
#         counts = Counter(lst)
#         return sorted(set(lst), key=lambda x: -counts[x])
#
#     def __call__(self):
#         nmr_list, rank_list = [], []
#         for self.hand in self.hand_list:
#             # print(self.hand)
#             nmr, rank = self.handrank()
#             nmr_list.append(nmr)
#             rank_list.append(rank)
#
#         index_max = max(range(len(nmr_list)), key=nmr_list.__getitem__)
#         nmr_max = nmr_list[index_max]
#         # print(nmr_list)
#
#         # royal flush is 10 .... high card is 1
#         if Counter(nmr_list)[nmr_max] > 1:  # untie equal hands
#             rep_idx = self.get_value_idx(nmr_max, nmr_list)
#
#             if nmr_max == 9 or nmr_max == 5 or nmr_max == 6 or nmr_max == 1:  # highest card in hand
#                 best = max(rep_idx, key=[max([card.value for card in hand]) for hand in self.hand_list].__getitem__)
#
#             elif nmr_max == 2 or nmr_max == 4 or nmr_max == 7 or nmr_max == 8:  # highest card in subset (pair, 3, 4 of a kind...)
#                 rep_idx = self.get_value_idx(nmr_max, nmr_list)
#                 max_list = [self.freq_sort([card.value for card in hand])[0] for hand in self.hand_list]
#                 if max_list[rep_idx[0]] == max_list[rep_idx[1]]:
#                     return rep_idx, nmr_max
#                 else:
#                     best = max(rep_idx, key=max_list.__getitem__)
#
#             elif nmr_max == 3:
#                 rep_idx = self.get_value_idx(nmr_max, nmr_list)
#                 max_list = [sorted(self.freq_sort([card.value for card in hand])[:2], reverse=True) for hand in self.hand_list]
#                 if max_list[rep_idx[0]][0] == max_list[rep_idx[1]][0]:
#                     if max_list[rep_idx[0]][1] == max_list[rep_idx[1]][1]:
#                         print("Not implemented: two pair double tie -> check 5th element")
#                         return rep_idx[0], nmr_max
#                     else:
#                         best = max(rep_idx, key=[lst[1] for lst in max_list].__getitem__)
#                 else:
#                     best = max(rep_idx, key=[lst[0] for lst in max_list].__getitem__)
#
#             else:
#                 return rep_idx
#
#             return best, nmr_max
#
#         else:
#             return index_max, nmr_max


#
# c1 = Card("clubs", 'a')
# c2 = Card("spades", 8)
# c3 = Card("spades", 4)
# c4 = Card("hearts", 8)
# c5 = Card("spades", 8)
# hand1 = [c1, c2, c3, c4, c5]
#
# c1 = Card("clubs", 2)
# c2 = Card("spades", 2)
# c3 = Card("spades", 6)
# c4 = Card("hearts", 'k')
# c5 = Card("spades", 'q')
# hand2 = [c1, c2, c3, c4, c5]
#
# c1 = Card("clubs", 8)
# c2 = Card("spades", 8)
# c3 = Card("spades", 8)
# c4 = Card("hearts", 'q')
# c5 = Card("spades", 9)
# hand3 = [c1, c2, c3, c4, c5]
#
# bh1 = BestHand([hand1, hand2, hand3])
# print("returns: ", bh1())

# hand1 = [c1, c2, c3, c4, c5]
# h1 = HandRank(hand1)
# print(h1.rank_hand())


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


# c1 = Card("clubs", 2)
# c2 = Card("spades", 2)
# c3 = Card("spades", 3)
# c4 = Card("hearts", 3)
# c5 = Card("spades", 9)
# hand1 = [c1, c2, c3, c4, c5]
#
# # c1 = Card("clubs", 2)
# # c2 = Card("spades", 2)
# # c3 = Card("spades", 6)
# # c4 = Card("hearts", 'k')
# # c5 = Card("spades", 'q')
# # hand2 = [c1, c2, c3, c4, c5]
#
# c1 = Card("clubs", 2)
# c2 = Card("spades", 2)
# c3 = Card("spades", 4)
# c4 = Card("hearts", 'a')
# c5 = Card("spades", 4)
# hand3 = [c1, c2, c3, c4, c5]
#
# bh1 = HandScore([hand1, hand3])
# print("returns: ", bh1())


# class ScoresCalc:
#
#     def calc(self):
#         for deck_cards in self.pd1():  # all possibilities for missing cards
#
#             if deck_cards is None:
#                 card_set = self.drawn_cards
#             else:
#                 card_set = self.drawn_cards + deck_cards
#             # print(deck_cards)
#             assert len(card_set) == 7
#
#             possible_hands = []
#             for hand in itertools.combinations(card_set, 5):  # find best hand for each possibility
#                 possible_hands.append(hand)
#             self.score_list.append(max(HandScore(possible_hands)()))
#
#         return self.score_list


class EvalScore:

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

    # def eval_adv_cards(self):
    #     adv_scores = []
    #     indiv_evals = []
    #     for adv_cards in self.adv_pd():
    #         # self.c += 1
    #         # print(self.c)
    #         # print(".")
    #         indiv_scores = self.private_calc(adv_cards=adv_cards)
    #         adv_scores.extend(indiv_scores)
    #
    #         indiv_hist, indiv_edge = np.histogram(indiv_scores, bins=500, range=(0, 110000))
    #         indiv_hist = indiv_hist / sum(indiv_hist)
    #         indiv_evals.append(sum(indiv_hist * indiv_edge[:-1]))
    #
    #     indiv_evals = np.array(indiv_evals)
    #     hist, self.adv_edges = np.histogram(adv_scores, bins=500, range=(0, 110000))
    #     self.adv_hist = hist/sum(hist)
    #     return sum(self.adv_hist * self.adv_edges[:-1]), np.std(indiv_evals)

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
            preflop_table = pd.read_csv("preflop_table.csv", names=["card1", "card2", "equity_avg", "equity_std"])
            pair_equity = preflop_table.loc[(preflop_table["card1"] == m1) & (preflop_table["card2"] == m2) | (preflop_table["card2"] == m1) & (preflop_table["card1"] == m2)]["equity_avg"]
            # print(pair_equity)

            sigma = (pair_equity.values[0] - 16699.046698432976) / 262.03557734030005
            print("#sigma: ", sigma)

            # print(sigma)

        else:
            time1 = time.time()
            my_eval = self.eval_my_cards()
            avg_eval, avg_std = self.eval_adv_cards()

            # print("My eval: ", my_eval)
            # print("Avg adv eval: ", avg_eval, " +/- ", avg_std)
            print("#sigma: ", (my_eval - avg_eval) / avg_std)
            # print("Time (s): ", time.time() - time1)
            self.show_odds()

# t1 = Card("clubs", 2)
# t2 = Card("spades", 'a')
# t3 = Card("hearts", 2)
# t4 = Card("spades", 'j')
# t5 = Card("spades", 2)

# m1 = Card("diamonds", 2)
# m2 = Card("clubs", 5)

# t1, t2, t3, t4, t5
# es1 = EvalScore(table_cards=[], my_cards=[m1, m2])
# es1()


def input_card(card_in):
    if card_in[0] == 'c':
        card_suit = "clubs"
    elif card_in[0] == 'd':
        card_suit = "diamonds"
    elif card_in[0] == 'h':
        card_suit = "hearts"
    elif card_in[0] == 's':
        card_suit = "spades"
    else:
        raise ValueError("ERROR: input suit not found")

    if card_in[1] == 'a':
        card_rank = 'A'
    elif card_in[1] == 'k':
        card_rank = 'K'
    elif card_in[1] == 'q':
        card_rank = 'Q'
    elif card_in[1] == 'j':
        card_rank = 'J'
    else:
        if len(card_in) == 2:
            card_rank = int(card_in[1])
        else:
            card_rank = int(card_in[1:])


    c1 = Card(suit=card_suit, rank=card_rank)
    return c1


def print_cards(my_cards, table_cards):
    print("\n ######################################")
    print("My cards:")
    for elem in my_cards:
        print("   ", elem)
    print("Table cards:")
    if len(table_cards) == 0:
        print("   None")
    else:
        for elem in table_cards:
            print("   ", elem)
    print("###################################### \n")



## get private cards
my_cards = []
for i in [1, 2]:
    new_card = input_card(input("Insert my card " + str(i)))
    my_cards.append(new_card)

print_cards(my_cards=my_cards, table_cards=[])
es1 = EvalScore(table_cards=[], my_cards=my_cards)
es1()

## flop
table_cards = []
for i in [1, 2, 3]:
    new_card = input_card(input("Insert table card " + str(i)))
    table_cards.append(new_card)

print_cards(my_cards=my_cards, table_cards=table_cards)
es1 = EvalScore(table_cards=table_cards, my_cards=my_cards)
es1()

## get 4th card
new_card = input_card(input("Insert table card 4"))
table_cards.append(new_card)

print_cards(my_cards=my_cards, table_cards=table_cards)
es1 = EvalScore(table_cards=table_cards, my_cards=my_cards)
es1()

## get 5th card
new_card = input_card(input("Insert table card 5"))
table_cards.append(new_card)

print_cards(my_cards=my_cards, table_cards=table_cards)
es1 = EvalScore(table_cards=table_cards, my_cards=my_cards)
es1()





# import time
# time1 = time.time()
# my_scores = ScoresCalc(table_cards=[t1, t2, t3], my_cards=[m1, m2])
# my_scores_list = my_scores()
# print(time.time()-time1)
#
# plt.figure()
# plt.hist(my_scores_list, bins=500, range=(0, 110000))


# t1 = Card("clubs", 2)
# t2 = Card("spades", 4)
# t3 = Card("hearts", 2)
#
# pd2 = PartialDeck(drawn_cards=[t1, t2, t3])
# player_scores_list = []
#
# # for player_cards in pd2():
# #     player_scores = ScoresCalc(table_cards=[t1, t2, t3], my_cards=player_cards)
# #     player_scores_list.extend(player_scores())
#
#
#
#
#
#
# plt.figure()
# hist, edges = np.histogram(my_scores_list, bins=500, range=(0, 110000))
# plt.plot(edges[:-1], hist/sum(hist), color='red')
# # plt.show()
# hist, edges = np.histogram(player_scores_list, bins=500, range=(0, 110000))
# plt.plot(edges[:-1], hist/sum(hist), color='blue')
# plt.show()
#
# # plt.hist(player_scores_list, bins=list(range(0, 100000, 10000)))
# # plt.show()
#



# d1 = Deck()
#
# player_list = [Player("rafael", 500), Player("leonardo", 500), Player("miguel", 500)]
# drawn_cards = []
# bets_sum = 0
#
# for player in player_list:
#     player.get_hand(d1)
#
# for round in range(6):
#
#     max_bet = 0
#     for idx, player in enumerate(player_list):
#         bet_value = player.place_bet(drawn_cards, max_bet)
#         if bet_value >= max_bet:
#             bets_sum += bet_value
#             max_bet = bet_value
#         else:
#             del player_list[idx]
#
#     if len(player_list) == 1:
#         player_list[0].balance += bets_sum
#
#     # print("drawn cards: ", drawn_cards)
#     # print("bet sum: ", bets_sum)
#     # for player in player_list:
#     #     print(player)
#     # print()
#     # print()
#
#     drawn_cards.append(d1())
#
# for player in player_list:
#
