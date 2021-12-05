import numpy as np
import itertools
import matplotlib.pyplot as plt
from scipy.stats import norm


def init_voters(
    candidates: tuple[str, ...],
    voters_count: int = 10000,
    distribution_function: str = "normal",
    dist=0,
    plot=False,
) -> tuple[np.ndarray, np.ndarray]:
    permutations = tuple(itertools.permutations(candidates))
    xs = np.arange(len(permutations))
    std = len(permutations) / 8
    mean = len(permutations) / 2
    n_peaks = 2
    # later we use n_peaks as a parameter, not done yet
    mean1 = len(perm)/(n_peaks + 1)
    mean2 = len(perm)/(n_peaks + 1)
    observations = np.array(np.zeros(len(permutations), dtype=int))
    if dist == 0:
        print(f"{permutations=}")
        if distribution_function == "normal":
            done = 0
            while done < voters_count:
                i = np.random.normal(mean, std)
                if i >= 0 and i <= len(permutations) - 1:
                    done += 1
                    observations[int(i)] += 1
    elif dist == 1:
        prob_dense = norm(loc=mean, scale=std)
        observations = [np.round(prob_dense.pdf(x) * voters_count) for x in xs]

        print(sum(j for j in observations))
        print(len(observations))
        print(observations)
    elif dist == 2:
        prob_dense_1 = norm(loc=mean1, scale=std)
        prob_dense_2 = norm(loc=mean2, scale=std)

        observations_1 = [np.round(prob_dense_1.pdf(
            x) * voters_count/n_peaks) for x in xs]
        observations_2 = [np.round(prob_dense_2.pdf(
            x) * voters_count/n_peaks) for x in xs]
        observations = [(i[0], i[1] + j[1])
                        for i, j in zip(observations_1, observations_2)]

        print(sum(j for j in observations))
        print(len(observations))
        print(observations)

    if plot:
        plt.scatter(np.arange(len(observations)), observations)
        plt.xticks(
            np.arange(len(permutations)),
            tuple(f'{" ".join(p)}' for p in permutations),
            rotation=45,
            ha="right",
        )
        plt.show()
    return np.array(permutations), observations


def test():
    preferences, voter_counts = init_voters(("A", "B", "C", "D"), plot=True)
    print(preferences)
    print(voter_counts)


if __name__ == "__main__":
    test()
