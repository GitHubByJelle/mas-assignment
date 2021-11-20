from argparse import ArgumentParser
from .tactical_voting_analyst import *

# from .candidate import *
from .voter import *
from .voting_schemes import VotingScheme
import numpy as np


def main():
    # E01.3
    # Set up Candidates
    candidates_names = (
        "A",
        "B",
        "C",
        "D",
    )  # will be used only for representation
    candidates = np.arange(
        len(candidates_names)
    )  # assign integer to each candidate, so we can use numpy
    preferences = np.array(
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
    voters = [Voter(np.expand_dims(preference, 0)) for preference in preferences]
    # Create TVA
    TVA = TacticalVotingAnalyst(candidates, candidates_names, voters)

    # print("\n", TVA.get_winner(np.array([3., 2., 1., 0.]), True))
    # print(TVA.overall_happiness())
    # TVA.determine_tactical_options(
    #     VotingScheme.borda_count, HappinessScheme.borda_count
    # )
    TVA.determine_paired_tactical_options(
        VotingScheme.borda_count, HappinessScheme.borda_count, 3
    )
    # print(f"{TVA.get_winners()=}")
    # for voting_scheme in VotingScheme:
    #     print(
    #         f"Overall happiness {voting_scheme} = {TVA.overall_happiness(voting_scheme)}"
    #     )

    """
    # E01.6
    # Set up Candidates
    candidates = [Candidate("A"), Candidate("B"), Candidate("C")]

    # Set up Voters
    voters = [
        Voter(np.array([[candidates[0], candidates[1], candidates[2]]])),
        Voter(np.array([[candidates[0], candidates[1], candidates[2]]])),
        Voter(np.array([[candidates[0], candidates[1], candidates[2]]])),
        Voter(np.array([[candidates[0], candidates[2], candidates[1]]])),
        Voter(np.array([[candidates[0], candidates[2], candidates[1]]])),
        Voter(np.array([[candidates[1], candidates[2], candidates[0]]])),
        Voter(np.array([[candidates[1], candidates[2], candidates[0]]])),
        Voter(np.array([[candidates[2], candidates[1], candidates[0]]])),
        Voter(np.array([[candidates[2], candidates[1], candidates[0]]])),
        Voter(np.array([[candidates[2], candidates[1], candidates[0]]])),
        Voter(np.array([[candidates[2], candidates[1], candidates[0]]])),
    ]

    # Create TVA
    TVA = TacticalVotingAnalyst(candidates, voters)

    print(TVA.get_winners())
    print(TVA.overall_happiness())
    """


if __name__ == "__main__":
    parser = ArgumentParser()
    args = parser.parse_args()
    main()
