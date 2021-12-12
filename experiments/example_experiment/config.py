import numpy as np
from tactical_voting_analyst.tactical_voting_analyst import TacticalVotingAnalyst
from tactical_voting_analyst.voting_schemes import VotingScheme
from tactical_voting_analyst.happiness_schemes import HappinessScheme
from experiment import ExperimentType

CANDIDATES_NAMES = (
    "A",
    "B",
    "C",
    "D",
)

CANDIDATES = np.arange(len(CANDIDATES_NAMES))

PREFERENCES = np.array(
    [
        [0, 1, 2, 3],
        [1, 2, 3, 0],
        [2, 3, 0, 1],
        [0, 1, 2, 3],
        [1, 2, 3, 0],
        [2, 3, 0, 1],
        [0, 1, 2, 3],
    ]
)

TVA = TacticalVotingAnalyst

VOTING_SCHEMES = [
    VotingScheme.borda_count,
    VotingScheme.plurality,
    VotingScheme.vote_for_two,
    VotingScheme.anti_plurality,
]

HAPPINESS_SCHEME = HappinessScheme.borda_count

EXPERIMENT_TYPE = ExperimentType.SIMPLE

TACTICAL_STRATEGY = "BASIC"

RISK_TYPE = 0
