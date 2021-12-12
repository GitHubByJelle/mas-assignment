import numpy as np
from tactical_voting_analyst.tactical_voting_analyst import TacticalVotingAnalyst
from tactical_voting_analyst.voting_schemes import VotingScheme
from tactical_voting_analyst.happiness_schemes import HappinessScheme
from tactical_voting_analyst.init_voters import (
    init_voters,
    DistributionTypes,
    sample_preferences,
)
from experiment import ExperimentType

CANDIDATES_NAMES = (
    ("A", "B", "C"),
    ("A", "B", "C", "D"),
    ("A", "B", "C", "D", "E"),
    ("A", "B", "C", "D", "E", "F"),
)

CANDIDATES = [np.arange(len(c)) for c in CANDIDATES_NAMES]
DISTRIBUTION = DistributionTypes.two_peaks

N_VOTERS = 10
PREFERENCES = sample_preferences(CANDIDATES_NAMES, DISTRIBUTION, N_VOTERS)
# PREFERENCES = (
#     np.array(
#         [
#             [0, 1, 2],
#             [1, 2, 0],
#             [2, 0, 1],
#             [0, 1, 2],
#             [1, 2, 0],
#             [2, 0, 1],
#             [0, 1, 2],
#         ]
#     ),
#     np.array(
#         [
#             [0, 1, 2, 3],
#             [1, 2, 3, 0],
#             [2, 3, 0, 1],
#             [0, 1, 2, 3],
#             [1, 2, 3, 0],
#             [2, 3, 0, 1],
#             [0, 1, 2, 3],
#         ]
#     ),
#     np.array(
#         [
#             [0, 1, 2, 3, 4],
#             [1, 2, 3, 4, 0],
#             [2, 3, 4, 0, 1],
#             [0, 1, 2, 3, 4],
#             [1, 2, 3, 4, 0],
#             [2, 3, 4, 0, 1],
#             [0, 1, 2, 3, 4],
#         ]
#     ),
#     np.array(
#         [
#             [0, 1, 2, 3, 4, 5],
#             [1, 2, 3, 4, 5, 0],
#             [2, 3, 4, 5, 0, 1],
#             [0, 1, 2, 3, 4, 5],
#             [1, 2, 3, 4, 5, 0],
#             [2, 3, 4, 5, 0, 1],
#             [0, 1, 2, 3, 4, 5],
#         ]
#     ),
# )

TVA = TacticalVotingAnalyst

VOTING_SCHEMES = [
    VotingScheme.borda_count,
    VotingScheme.plurality,
    VotingScheme.vote_for_two,
    VotingScheme.anti_plurality,
]

HAPPINESS_SCHEME = HappinessScheme.linear_weight

EXPERIMENT_TYPE = ExperimentType.INCREASE_CANDIDATES

TACTICAL_STRATEGY = "BASIC"

RISK_TYPE = 2
