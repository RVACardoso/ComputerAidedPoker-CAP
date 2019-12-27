from sigmascores import Card
from profitscores import ProfitScore
import numpy as np


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


current_cost = 0


def eval_cards(my_cards, table_cards, n_players):
    print_cards(my_cards=my_cards, table_cards=table_cards)
    es1 = ProfitScore(table_cards=table_cards, my_cards=my_cards, n_players=n_players)

    money_feat = input("Insert pot_total and round bets: \n")
    money_feat = [float(val) for val in money_feat.split()]
    while money_feat != "x":
        pot_total = money_feat[0]
        round_bets = money_feat[1:]
        round_bets_avg = np.average(round_bets)
        while len(round_bets) < (n_players-1):
            round_bets.append(round_bets_avg)

        global current_cost
        print(es1(pot_total, round_bets, current_cost))
        current_cost += float(input("Bet value (larger or equal to " + str(np.max(round_bets)) + ") \n"))

        money_feat = input("Insert pot_total and round bets: (insert 'x' for next stage)\n")
        try:
            money_feat = [float(val) for val in money_feat.split()]
        except ValueError:
            break


player_count = int(input("Number of players: "))

## get private cards

my_cards = []
for i in [1, 2]:
    new_card = input_card(input("Insert my card " + str(i)))
    my_cards.append(new_card)

eval_cards(my_cards=my_cards, table_cards=[], n_players=player_count)

## flop

table_cards = []
for i in [1, 2, 3]:
    new_card = input_card(input("Insert table card " + str(i)))
    table_cards.append(new_card)

eval_cards(my_cards=my_cards, table_cards=table_cards, n_players=player_count)

## get 4th card

new_card = input_card(input("Insert table card 4"))
table_cards.append(new_card)

eval_cards(my_cards=my_cards, table_cards=table_cards, n_players=player_count)

## get 5th card

new_card = input_card(input("Insert table card 5"))
table_cards.append(new_card)

eval_cards(my_cards=my_cards, table_cards=table_cards, n_players=player_count)
