import numpy as np
import matplotlib.pyplot as plt


def random_normal_gen(avg, std, size):
    for _ in range(size):
        yield np.random.normal(avg, std)


n_players = 5

## stay_adv_money score expected distribution

# adv_money_list = []
# for avg in range(2, 10):
#     print(avg)
#     for std in range(1, 5):
#         for _ in range(50000):
#             round_bets = np.array([i for i in random_normal_gen(avg, std, n_players) if i > 0])  # unit is number of big blinds
#             if len(round_bets) != 0:
#                 round_max = np.max(round_bets)
#                 round_avg = np.average(round_bets)
#                 stay_adv_money = 1.0/(round_max * round_avg)
#                 adv_money_list.append(stay_adv_money)
#
# hist1, edges1 = np.histogram(adv_money_list, range=(0, 0.15), bins=200)
#
# total_sum = np.sum(hist1)
# fraction_sum = np.array([np.sum(hist1[:i])/total_sum for i in range(len(hist1))])
#
# final_edges = edges1[:-1: 5]
# final_fraction_sum = fraction_sum[::5]
#
# for edge, frac in zip(final_edges, final_fraction_sum):
#     print("{},{}".format(edge, frac))
#
# plt.plot(final_edges, final_fraction_sum)
# plt.show()
#

## stay my money score expected distribution

n_players = 5

stay_my_money_list = []
for avg in range(2, 10):
    print(avg)
    for std in range(1, 5):
        for _ in range(50000):
            n_rounds = np.random.randint(1, 5)
            current_cost = 0
            pot_total = 0
            for _ in range(n_rounds):
                round_bets = np.array([i for i in random_normal_gen(avg, std, n_players) if i > 0])  # unit is number of big blinds
                if len(round_bets) != 0:
                    round_max = np.max(round_bets)
                    current_cost += round_bets[0]
                    pot_total += np.sum(round_bets)
            stay_my_money = (current_cost * pot_total)/(round_max*n_players)
            stay_my_money_list.append(stay_my_money)

hist1, edges1 = np.histogram(stay_my_money_list, range=(0, 250), bins=200)

total_sum = np.sum(hist1)
fraction_sum = np.array([np.sum(hist1[:i])/total_sum for i in range(len(hist1))])

final_edges = edges1[:-1: 2]
final_fraction_sum = fraction_sum[::2]

for edge, frac in zip(final_edges, final_fraction_sum):
    print("{},{}".format(edge, frac))

plt.plot(final_edges, final_fraction_sum)
# plt.plot(edges1[:-1], hist1)
plt.show() 
