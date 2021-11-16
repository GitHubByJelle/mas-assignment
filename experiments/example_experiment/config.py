import numpy as np
from tactical_voting_analyst.tactical_voting_analyst import TacticalVotingAnalyst
from tactical_voting_analyst.voting_schemes import VotingScheme

CANDIDATES_NAMES = (
    "A",
    "B",
    "C",
    "D",
) 

CANDIDATES = np.arange(
    len(CANDIDATES_NAMES)
)

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

VOTING_SCHEMES = [VotingScheme.borda_count,
                    VotingScheme.plurality, 
                    VotingScheme.vote_for_two, 
                    VotingScheme.anti_plurality]