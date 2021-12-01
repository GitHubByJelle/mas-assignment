import numpy as np
import itertools
from scipy import stats
import matplotlib.pyplot as plt


def init_voters(
    candidates: tuple[str, ...],
    total_number_of_voters: int = 10000,
    distribution_function: str = "normal",
) -> tuple[np.ndarray, np.ndarray]:
    permutations = tuple(itertools.permutations(candidates))

    vals = np.array(tuple(0 for _ in range(len(permutations))))
    print(f"{permutations=}")
    if distribution_function == "normal":
        std = len(permutations) / 8
        loc = len(permutations) / 2
        vals = np.array(tuple(0 for _ in range(len(permutations))))
        done = 0
        while done < total_number_of_voters:
            i = np.random.normal(loc, std)
            if i >= 0 and i <= len(permutations) - 1:
                done += 1
                vals[int(i)] += 1
        plt.plot(np.arange(len(vals)), vals)
        plt.xticks(
            np.arange(len(permutations)),
            tuple(f'"{" ".join(p)}"' for p in permutations),
            rotation=45,
            ha="right",
        )
        # plt.show()
    return np.array(permutations), vals


def test():
    preferences, voter_counts = init_voters(("A", "B", "C", "D"))
    print(preferences)
    print(voter_counts)


if __name__ == "__main__":
    test()
