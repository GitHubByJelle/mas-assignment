from enum import Enum

import numpy as np
import matplotlib.pyplot as plt
from tactical_voting_analyst.tactical_voting_analyst import TacticalVotingAnalyst
from tactical_voting_analyst.voting_schemes import VotingScheme
from tactical_voting_analyst.happiness_schemes import HappinessScheme
from experiment import ExperimentType
from tactical_voting_analyst.init_voters import init_voters, DistributionTypes
from tqdm import tqdm


########### CONFIG ###########
HAPPINESS_SCHEME = HappinessScheme.cubed_weight
DISTRIBUTION_F = DistributionTypes.normal
CANDIDATES_NAMES = (("A", "B", "C"), ("A", "B", "C", "D"), ("A", "B", "C", "D", "E"))
VOTERS = [10, 16, 24]
##############################

IMAGE_ID = 2


def get_impact(candidates, preferences):
    TVA = TacticalVotingAnalyst(candidates=np.arange(len(candidates)),
                                candidate_names=candidates,
                                preferences=preferences)
    impact = []
    for V_scheme in VotingScheme:
        impact.append(TVA.impact_overall_happiness(voting_scheme=V_scheme,
                                                   happiness_scheme=HAPPINESS_SCHEME))
    impact = [x * 100 for x in impact]
    return impact


def get_preferences(candidates, n_voters):
    preferences, voter_counts, observations = init_voters(
        candidates,
        distribution_function=DISTRIBUTION_F,
        voters_count=n_voters,
        plot=False,
    )
    new_preferences = []
    for voter in list(observations):
        a = []
        for ch in voter:
            id = 0
            if ch == 'B': id = 1
            elif ch == 'C': id = 2
            elif ch == 'D': id = 3
            a.append(id)
        new_preferences.append(a)
    return np.array(new_preferences)


def increase_candidates():
    print(ExperimentType.INCREASE_CANDIDATES)
    episodes = []
    for i, candidates in enumerate(CANDIDATES_NAMES):
        not_important_list = []
        print("*******************")
        for j in tqdm(range(1000), desc="Increase candidates"):
            preferences = get_preferences(candidates, VOTERS[0])
            not_important_list.append(get_impact(candidates, preferences))
        impact = np.average(not_important_list, axis=0)
        episodes.append(impact)
        print("Candidates: ", candidates)
        print("# voters: ", str(VOTERS[0]))
        print("Impact: ", impact)

    plot_bars(episodes, ExperimentType.INCREASE_CANDIDATES)


def increase_voters():
    print(ExperimentType.INCREASE_VOTERS)
    episodes = []
    candidates = CANDIDATES_NAMES[1]
    for i in range(3):
        not_important_list = []
        for j in tqdm(range(1000), desc="Increase voters"):
            preferences = get_preferences(candidates, VOTERS[i])
            not_important_list.append(get_impact(candidates, preferences))
        impact = np.average(not_important_list, axis=0)
        episodes.append(impact)
        print("*******************")
        print("Candidates: ", candidates)
        print("# voters: ", str(VOTERS[i]))
        print("Impact: ", impact)

    plot_bars(episodes, ExperimentType.INCREASE_VOTERS)


def plot_bars(episodes, experiment_type):
    # plot parameters
    labels = ('plurality', 'vote_for_two', 'borda_count', 'anti_plurality')
    y_pos = np.arange(len(labels))
    fig, ax = plt.subplots(figsize=(10, 5))
    width = 0.2
    N = 12
    EXPERIMENT_NAME = DISTRIBUTION_F.name + ' distribution and '
    if experiment_type == ExperimentType.INCREASE_CANDIDATES:
        EXPERIMENT_NAME += str(VOTERS[0]) + ' voters'
    else:
        EXPERIMENT_NAME += str(len(CANDIDATES_NAMES[2])) + ' candidates'
    for i in range(len(episodes)):
        impact = episodes[i]
        print("Impact = ", impact)
        xs = y_pos + width * i
        ys = impact

        label_ = str(len(CANDIDATES_NAMES[i])) + ' candidates' if experiment_type == ExperimentType.INCREASE_CANDIDATES \
            else str(VOTERS[i]) + ' voters'
        ax.barh(xs, ys, width, align='center', label=label_)
        ax.plot(impact, y_pos + width * i, 's', markersize=7)
        for i, j in zip(ys, xs):
            ax.annotate(str(np.round(i, 3)), xy=(i, j),
                        horizontalalignment='right',
                        verticalalignment='bottom', size=10)
        ax.set_yticks(y_pos + width, labels=labels)
        ax.invert_yaxis()
        N += 4
    ax.set_xlabel('Impact')
    # ax.set_title(EXPERIMENT_NAME)
    ax.legend()
    ax.axvline(0, color='k', linewidth=1)
    plt.title(EXPERIMENT_NAME)
    plt.suptitle('Impact Overall Happiness')
    # plt.show()
    global IMAGE_ID
    plt.savefig('OverallHappiness_'+ str(IMAGE_ID)+ '.png')
    IMAGE_ID += 1


increase_candidates()
print()
print()
increase_voters()


