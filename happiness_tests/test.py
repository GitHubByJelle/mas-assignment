import numpy as np
from numpy.random.mtrand import f
from tqdm import tqdm
import ipdb
from time import time
import matplotlib.pyplot as plt
from argparse import ArgumentParser


def borda_h_v1(borda, true_preferences, ranked_candidates_id):
    old_happiness = 0
    for i, candidate in enumerate(true_preferences):
        old_happiness += (
            borda[i] * borda[np.nonzero(ranked_candidates_id == candidate)[0][0]]
        )
    return old_happiness


def linear_weigth_v1(weights, true_preferences, ranked_candidates_id):
    happiness = 0
    for i, candidate in enumerate(true_preferences):
        outcome_index = np.where(ranked_candidates_id == candidate)
        happiness += weights[i] * (i - outcome_index[0][0])
    return happiness


def squared_weight_v1(weights, true_preferences, ranked_candidates_id):
    happiness = 0
    for i, candidate in enumerate(true_preferences):
        outcome_index = np.where(ranked_candidates_id == candidate)
        happiness += weights[i] * (i - outcome_index[0][0])
    return happiness


def squared_weight_v2(weights, true_preferences, ranked_candidates_id):
    argsorting = np.arange(len(ranked_candidates_id))
    argsorting[ranked_candidates_id] = argsorting.copy()
    indices = argsorting[true_preferences]
    return np.dot(weights, np.arange(len(true_preferences)) - indices)


def linear_weigth_v2(weights, true_preferences, ranked_candidates_id):
    argsorting = np.arange(len(ranked_candidates_id))
    argsorting[ranked_candidates_id] = argsorting.copy()
    indices = argsorting[true_preferences]
    return np.dot(weights, np.arange(len(true_preferences)) - indices)


def get_linear():
    n = 100
    ranked_candidates_id = np.arange(n)
    np.random.shuffle(ranked_candidates_id)
    true_preferences = np.arange(n)
    np.random.shuffle(true_preferences)
    weights = np.arange(len(ranked_candidates_id), 0, -1)
    old_happiness, p1 = performance(
        linear_weigth_v1, weights, true_preferences, ranked_candidates_id
    )
    happiness, p2 = performance(
        linear_weigth_v2, weights, true_preferences, ranked_candidates_id
    )
    """
    new_happiness, p3 = performance(
        borda_h_v3, borda, true_preferences, ranked_candidates_id
    )
    """

    ## END OLD
    assert old_happiness == happiness, f"not equal :( {old_happiness} {happiness}"
    # print(old_happiness)
    # print(happiness)
    # borda_ranking =
    return p1, p2


def run_test(test_fn, name):
    performances = []
    for _ in tqdm(range(100000)):
        performances.append(test_fn())
    avg_perf = np.mean(np.array(performances).T, 1)
    print(f"relative_perf {avg_perf[-1]/avg_perf[0]}")
    plt.bar(np.arange(len(performances[0])), avg_perf)
    plt.title(f"{name} performance against version")
    plt.savefig(f"{name}.png")


def get_squared():
    n = 100
    ranked_candidates_id = np.arange(n)
    np.random.shuffle(ranked_candidates_id)
    true_preferences = np.arange(n)
    np.random.shuffle(true_preferences)
    weights = np.square(np.arange(len(ranked_candidates_id), 0, -1))
    old_happiness, p1 = performance(
        squared_weight_v1, weights, true_preferences, ranked_candidates_id
    )
    happiness, p2 = performance(
        squared_weight_v2, weights, true_preferences, ranked_candidates_id
    )
    """
    new_happiness, p3 = performance(
        borda_h_v3, borda, true_preferences, ranked_candidates_id
    )
    """

    ## END OLD
    assert old_happiness == happiness, f"not equal :( {old_happiness} {happiness}"
    # print(old_happiness)
    # print(happiness)
    # borda_ranking =
    return p1, p2


def borda_h_v2(borda, true_preferences, ranked_candidates_id):
    borda_preferences = borda[np.argsort(true_preferences)]
    borda_ranking = borda[np.argsort(ranked_candidates_id)]
    happiness = np.dot(borda_preferences, borda_ranking)
    return happiness


def borda_h_v3(borda, true_preferences, ranked_candidates_id):
    argsorting = np.arange(len(ranked_candidates_id))
    argsorting[ranked_candidates_id] = argsorting.copy()
    indices = argsorting[true_preferences]
    return np.dot(borda, borda[indices])


def performance(fn, borda, true_preferences, ranked_candidates_id):
    t0 = time()
    result = fn(borda, true_preferences, ranked_candidates_id)
    t1 = time()
    return result, (t1 - t0)


def get_borda():
    n = 100
    ranked_candidates_id = np.arange(n)
    np.random.shuffle(ranked_candidates_id)
    true_preferences = np.arange(n)
    np.random.shuffle(true_preferences)
    borda = np.arange(len(ranked_candidates_id) - 1, -1, -1)

    old_happiness, p1 = performance(
        borda_h_v1, borda, true_preferences, ranked_candidates_id
    )
    happiness, p2 = performance(
        borda_h_v2, borda, true_preferences, ranked_candidates_id
    )
    new_happiness, p3 = performance(
        borda_h_v3, borda, true_preferences, ranked_candidates_id
    )

    ## END OLD
    assert old_happiness == happiness == new_happiness, "not equal :("
    # print(old_happiness)
    # print(happiness)
    # borda_ranking =
    return p1, p2, p3


"""
def test_borda():
    performances = []
    for _ in tqdm(range(100000)):
        performances.append(get_borda())
    avg_perf = np.mean(np.array(performances).T, 1)
    print(f"relative_perf {avg_perf[-1]/avg_perf[0]}")
    plt.bar(np.arange(3), avg_perf)
    plt.title("borda performance against version")
    plt.savefig("borda_performances.png")
"""


def main():
    parser = ArgumentParser()
    parser.add_argument("test_type", choices=("borda", "linear", "squared"))
    args = parser.parse_args()
    if args.test_type == "borda":
        run_test(get_borda, "borda")
    elif args.test_type == "linear":
        run_test(get_linear, "linear")
    elif args.test_type == "squared":
        run_test(get_squared, "squared")


if __name__ == "__main__":
    main()
