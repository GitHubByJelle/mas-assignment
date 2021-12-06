import numpy as np
import matplotlib.pyplot as plt
from tactical_voting_analyst.tactical_voting_analyst import TacticalVotingAnalyst
from tactical_voting_analyst.voting_schemes import VotingScheme
from tactical_voting_analyst.happiness_schemes import HappinessScheme
from experiment import ExperimentType

########### CONFIG ###########
HAPPINESS_SCHEME = HappinessScheme.cubed_weight
EXPERIMENT_TYPE = ExperimentType.INCREASE_VOTERS
##############################

EXPERIMENT_NAME = 'Impact Overall Happiness, ' + EXPERIMENT_TYPE.name
labels = ('plurality', 'vote_for_two', 'borda_count', 'anti_plurality')
y_pos = np.arange(len(labels))
fig, ax = plt.subplots(figsize=(10, 5))
width = 0.2

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
        n_voters = len(PREFERENCES[i])
        print("********************")
        print(str(n_candidates) + ' candidates')
        TVA = TacticalVotingAnalyst(CANDIDATES[i], CANDIDATES_NAMES[i], PREFERENCES[i])
        impact = []
        for V_scheme in VotingScheme:
            impact.append(TVA.impact_overall_happiness(voting_scheme=V_scheme,
                                                       happiness_scheme=HAPPINESS_SCHEME))
        impact = [x * 100 for x in impact]
        print("Impact = ", impact)
        xs = y_pos + width*i
        ys = impact
        ax.barh(xs, ys, width, align='center', label=str(n_candidates)+' candidates')
        ax.plot(impact, y_pos + width*i, 's', markersize=7)
        for i, j in zip(ys, xs):
            ax.annotate(str(np.round(i, 3)), xy=(i, j),
                        horizontalalignment='right',
                        verticalalignment='bottom', size=10)
        ax.set_yticks(y_pos + width, labels=labels)
        ax.invert_yaxis()
    ax.set_xlabel('Impact')
    ax.set_title(EXPERIMENT_NAME)
    ax.legend()
    ax.axvline(0, color='k', linewidth=1)


elif EXPERIMENT_TYPE == ExperimentType.INCREASE_VOTERS:
    CANDIDATES_NAMES = (
        "A",
        "B",
        "C",
        "D",
    )

    CANDIDATES = np.arange(len(CANDIDATES_NAMES))

    PREFERENCES = [
        np.array([[0, 1, 2, 3], [1, 2, 3, 0], [2, 3, 0, 1], [0, 1, 2, 3]]),
        np.array([[0, 1, 2, 3], [1, 2, 3, 0], [2, 3, 0, 1],
                  [0, 1, 2, 3], [1, 2, 3, 0], ]),
        np.array(
            [
                [2, 1, 0, 3],
                [1, 2, 3, 0],
                [2, 3, 0, 1],
                [0, 1, 2, 3],
                [2, 1, 3, 0],
                [2, 3, 0, 1],
                [0, 1, 2, 3],
            ]
        ),
    ]

    for i in range(len(PREFERENCES)):
        n_candidates = len(CANDIDATES)
        n_voters = len(PREFERENCES[i])
        print("********************")
        print(str(n_voters) + ' voters')
        TVA = TacticalVotingAnalyst(CANDIDATES, CANDIDATES_NAMES, PREFERENCES[i])
        impact = []
        for V_scheme in VotingScheme:
            impact.append(TVA.impact_overall_happiness(voting_scheme=V_scheme,
                                                                 happiness_scheme=HAPPINESS_SCHEME))
        impact = [x * 100 for x in impact]
        print("Impact = ", impact)
        xs = y_pos + width*i
        ys = impact
        ax.barh(xs, ys, width, align='center', label=str(n_voters)+' voters')
        ax.plot(impact, y_pos + width*i, 's', markersize=7)
        for i, j in zip(ys, xs):
            ax.annotate(str(np.round(i, 3)), xy=(i, j),
                        horizontalalignment='right',
                        verticalalignment='bottom', size=10)
        ax.set_yticks(y_pos + width, labels=labels)
        ax.invert_yaxis()
    ax.set_xlabel('Impact')
    ax.set_title(EXPERIMENT_NAME)
    ax.legend()
    ax.axvline(0, color='k', linewidth=1)

# plt.show()
plt.savefig(EXPERIMENT_TYPE.name + '.png')
