import numpy as np
import matplotlib.pyplot as plt
from tactical_voting_analyst.tactical_voting_analyst import TacticalVotingAnalyst
from tactical_voting_analyst.voting_schemes import VotingScheme
from tactical_voting_analyst.happiness_schemes import HappinessScheme
from experiment import ExperimentType


def bar_plot(happiness_scheme: HappinessScheme,
             ys,
             n_voters: int, n_candidates: int):
    """
    :param voting_scheme:
    :param happiness_scheme:
    :param ys: i.e  (5, 4, 3, 5)
    :param labels: i.e. ('a', 'b', 'c', 'd')
    :return:
    """
    labels = ('plurality', 'vote_for_two', 'borda_count', 'anti_plurality')

    width = 1
    xs = np.arange(len(labels))
    plt.bar(xs, ys, width, align='center', color='blue')

    plt.xticks(xs, labels)
    plt.yticks(ys)
    plt.title("Impact Overall Happiness")
    plt.suptitle("Happiness scheme = " + happiness_scheme.name +
                 ", # voters = " + str(n_voters) + ", # candidates = " + str(n_candidates))
    plt.show()
    # plt.savefig('netscore.png')


EXPERIMENT_TYPE = ExperimentType.INCREASE_CANDIDATES

if EXPERIMENT_TYPE == ExperimentType.INCREASE_CANDIDATES:

    CANDIDATES_NAMES = (("A", "B", "C"), ("A", "B", "C", "D"),
                        ("A", "B", "C", "D", "E"))

    CANDIDATES = [np.arange(len(c)) for c in CANDIDATES_NAMES]

    PREFERENCES = (
        np.array(
            [[0, 1, 2], [1, 2, 0], [2, 0, 1], [0, 1, 2],
             [1, 2, 0], [2, 0, 1], [0, 1, 2], ]
        ),
        np.array(
            [
                [0, 1, 2, 3],
                [1, 2, 3, 0],
                [2, 3, 0, 1],
                [0, 1, 2, 3],
                [1, 2, 3, 0],
                [2, 3, 0, 1],
                [0, 1, 2, 3],
            ]
        ),
        np.array(
            [
                [0, 1, 2, 3, 4],
                [1, 2, 3, 4, 0],
                [2, 3, 4, 0, 1],
                [0, 1, 2, 3, 4],
                [1, 2, 3, 4, 0],
                [2, 3, 4, 0, 1],
                [0, 1, 2, 3, 4],
            ]
        ),
    )

    for i in range(len(CANDIDATES)):
        n_candidates = len(CANDIDATES[i])
        n_voters = len(PREFERENCES[0])
        TVA = TacticalVotingAnalyst(CANDIDATES[i], CANDIDATES_NAMES[i], PREFERENCES[i])
        H_scheme = HappinessScheme.squared_weight
        impact = []
        for V_scheme in VotingScheme:
            impact.append(TVA.impact_overall_happiness(voting_scheme=V_scheme,
                                                       happiness_scheme=H_scheme))
        bar_plot(H_scheme, impact, n_voters, n_candidates)

elif EXPERIMENT_TYPE == ExperimentType.INCREASE_VOTERS:
    pass
