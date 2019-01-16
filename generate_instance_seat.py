from graph_class import Graph
from members import *
import graph
import collections
import random
import numpy as np

random.seed(1000)

def seat_model_generator(n1, n2, k_low, k_up):
    """
    create a graph with the partition R of size n1 and
    partition H of size n2 using the model as described in
    Marriage, Honesty, and Stability
    Immorlica, Nicole and Mahdian, Mohammad
    Sixteenth Annual ACM-SIAM Symposium on Discrete Algorithms
    :param n1: size of partition R
    :param n2: size of partition H
    """
    def order_by_master_list(l, master_list):
        return sorted(l, key=master_list.index)

    possibile_credits = [5, 10, 15, 20]
    probs = np.random.geometric(p=0.10, size=len(possibile_credits))
    probs = probs / np.sum(probs)

    def get_hosp_credits():
        return list(np.random.choice(possibile_credits, size=1, replace=False, p=probs))[0]

    def get_hosp_capacity_uniform():
        res_cap_sum = 0
        hosp_cred_sum = 0
        for r in g.residents:
            res_cap_sum += r.uq
        for h in g.hospitals:
            hosp_cred_sum += h.credits

        return int(np.ceil((2.5 * res_cap_sum) / hosp_cred_sum))

    def get_hosp_capacity_non_uniform(cap):
        low = int(np.ceil(0.3*cap))
        high = int(np.ceil(1.7*cap))
        return random.randint(low, high)

    g = Graph()

    # default hospital capacity
    cap = 60

    # create the sets R and H, r_1 ... r_n1, h_1 .. h_n2
    R = list('r{}'.format(i) for i in range(1, n1+1))
    H = list('h{}'.format(i) for i in range(1, n2+1))

    for res in R:
        g.residents.append(Resident(res))

    for hosp in H:
        g.hospitals.append(Hospital(hosp, 0, cap, get_hosp_credits()))

    # prepare a master list
    master_list = list(r for r in R)
    random.shuffle(master_list)

    # setup a probability distribution over the hospitals
    p = np.random.geometric(p=0.10, size=len(H))

    # normalize the distribution
    p = p / np.sum(p)  # p is a ndarray, so this operation is correct

    prob_dict = dict(zip(H, p))
    master_list_h = sorted(H, key=lambda h: prob_dict[h], reverse=True)
    # print(prob_dict, master_list_h, sep='\n')

    pref_H, pref_R = collections.defaultdict(list), {}
    for r in R:
        # sample women according to the probability distribution and without replacement
        k = random.randint(k_low, k_up)
        pref_R[r] = list(np.random.choice(H, size=min(len(H), k), replace=False, p=p))
        # add these man to the preference list for the corresponding women
        for h in pref_R[r]:
            pref_H[h].append(r)

    for r in R:
        # pref_R[r] = order_by_master_list(pref_R[r], master_list_h)
        random.shuffle(pref_R[r])
        res = g.get_resident(r)
        for hosp in pref_R[r]:
            res.pref.append(g.get_hospital(hosp))

    for h in H:
        # pref_H[h] = order_by_master_list(pref_H[h], master_list)
        random.shuffle(pref_H[h])
        hosp = g.get_hospital(h)
        for res in pref_H[h]:
            hosp.pref.append(g.get_resident(res))

    g.init_resident_capacities()

    # uniform capacity for courses
    cap = get_hosp_capacity_uniform()
    for h in g.hospitals:
        h.uq = get_hosp_capacity_non_uniform(cap)

    g.init_all_resident_class()
    g.init_master_classes_random()
    return g


def main():
    import sys
    if len(sys.argv) < 4:
        print("usage: {} <n1> <n2> <k_low> <k_up>".format(sys.argv[0]), file=sys.stderr)
    else:
        n1, n2, k_low, k_up = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4])
        G = seat_model_generator(n1, n2, k_low, k_up)
        G.print_format()

if __name__ == '__main__':
    main()
