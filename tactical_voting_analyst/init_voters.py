import numpy as np
import itertools
import matplotlib.pyplot as plt
from scipy.stats import norm
from enum import Enum
from .voting_schemes import VotingScheme
from .tactical_voting_analyst import HappinessScheme
from .tactical_voting_analyst import TacticalVotingAnalyst as TVA
import ipdb

# TODO: design an experiment for this


class DistributionTypes(Enum):
    normal = "normal"
    uniform = "uniform"
    two_peaks = "two_peaks"


def init_voters(
    candidates: tuple[str, ...],
    voters_count: int = 1000,
    distribution_function: DistributionTypes = DistributionTypes.normal,
    stochastic=False,
    plot=False,
) -> tuple[np.ndarray, np.ndarray]:
    permutations = np.array(tuple(itertools.permutations(candidates)))
    np.random.shuffle(permutations)
    xs = np.arange(len(permutations))
    std = len(permutations) / 8
    mean = len(permutations) / 2
    observations = np.array(np.zeros(len(permutations), dtype=int))
    if stochastic:
        print(f"{permutations=}")
        if distribution_function == "normal":
            done = 0
            while done < voters_count:
                i = np.random.normal(mean, std)
                if i >= 0 and i <= len(permutations) - 1:
                    done += 1
                    observations[int(i)] += 1
    else:
        pdf = lambda x: x
        if distribution_function == DistributionTypes.normal:
            pdf = norm(loc=mean, scale=std).pdf
        elif distribution_function == DistributionTypes.uniform:
            pdf = lambda x: np.zeros(len(x)) + 1 / len(xs)
        elif distribution_function == DistributionTypes.two_peaks:
            # TODO:
            n_peaks = 2
            mean = len(permutations) / (n_peaks + 1)
            mean2 = 2 * (len(permutations) / (n_peaks + 1))
            sd = (len(permutations) / 2) / (3 * n_peaks)
            pdf_1 = norm(loc=mean, scale=sd).pdf
            # prob_dense = norm(loc=mean, scale=sd)

            # Creating the second distribution
            pdf_2 = norm(loc=mean2, scale=sd).pdf
            # prob_dense_2 = norm(loc=mean2, scale=sd)
            pdf = lambda x: (pdf_1(x) + pdf_2(x)) / n_peaks

        observations = (pdf(xs) * voters_count).astype(int)
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
        plt.savefig("../happiness_distribution.png")
        plt.show()
    return permutations, observations.astype(int)


def test():
    preferences, voter_counts = init_voters(
        ("A", "B", "C", "D"),
        distribution_function=DistributionTypes.uniform,
        plot=True,
    )
    print(preferences)
    print(voter_counts)


def experiment():
    candidates = ("A", "B", "C", "D")
    happinesses = []
    for distribution_function in DistributionTypes:
        preferences, voter_counts = init_voters(
            candidates, distribution_function=distribution_function
        )
        proto_preferences = tuple(
            v * (tuple(candidates.index(c) for c in p),)
            for p, v in zip(preferences, voter_counts)
        )
        new_preferences: list[tuple[int, ...]] = []
        for ps in proto_preferences:
            new_preferences.extend(ps)
        tva = TVA(
            candidates=np.arange(len(candidates)),
            candidate_names=candidates,
            preferences=tuple(new_preferences),
        )
        happinesses.append(
            (
                distribution_function,
                tva.overall_happiness(
                    VotingScheme.borda_count, HappinessScheme.cubed_weight
                ),
            )
        )
        print(f"{distribution_function} Happiness:{happinesses[-1][1]}")
    plt.bar(
        np.arange(len(happinesses)),
        [h[1] for h in happinesses],
        tick_label=[h[0] for h in happinesses],
    )
    plt.show()


if __name__ == "__main__":
    experiment()
