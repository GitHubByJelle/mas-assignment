import string
from argparse import ArgumentParser
from .tactical_voting_analyst import TacticalVotingAnalyst

# from .candidate import *
from .voter import *
from .voting_schemes import VotingScheme
from .init_voters import init_voters, DistributionTypes
import numpy as np


def main(
    candidates_count: int,
    voters_count: int,
    distribution_name: str,
    happiness_scheme_name: str,
    voting_scheme_name: str,
):

    candidates_names = tuple(string.ascii_uppercase[:candidates_count])
    # E01.3
    # Set up Candidates

    distribution_type = DistributionTypes.__dict__[distribution_name]
    happiness_scheme = HappinessScheme.__dict__[happiness_scheme_name]
    voting_scheme = VotingScheme.__dict__[voting_scheme_name]

    frequencies, voters_count, observations = init_voters(
        candidates=candidates_names,
        voters_count=voters_count,
        distribution_function=distribution_type,
    )
    tva = TacticalVotingAnalyst(
        candidates=np.arange(len(candidates_names)),
        candidate_names=candidates_names,
        preferences=observations,
        verbose=True,
    )
    # Create TVA
    tactical_options = tva.determine_tactical_options(
        VotingScheme.borda_count, HappinessScheme.borda_count
    )
    risks = [
        tva.calculate_risk(
            tactical_options, voting_scheme, happiness_scheme, version=i,
        )
        for i in range(3)
    ]
    print(
        f"The 3 types of risks are (see the report): {[round(r, 4) for r in risks]}"
    )

    # print(TVA.overall_happiness())
    # TVA.determine_tactical_options(
    #     VotingScheme.borda_count, HappinessScheme.borda_count
    # )
    # TVA.determine_tactical_options(
    #     VotingScheme.borda_count, HappinessScheme.borda_count
    # )

    # TVA.voting_situation.get_impact_tactical_options_majority_table(TVA.determine_tactical_options(
    #     VotingScheme.borda_count, HappinessScheme.borda_count
    # ))
    """
    for i, t_opts in enumerate(
        TVA.determine_tactical_options_run_off_election(
            np.array(preferences), HappinessScheme.borda_count
        )
    ):
        print("Voter {}".format(i))
        for t_opt in t_opts:
            print(t_opt)
        print()
    """
    # TVA.voting_situation.create_majority_graph_preferences(TVA.voting_situation.determine_majority_table())
    # TVA.voting_situation.create_majority_graph_preferences(
    #     TVA.voting_situation.get_impact_tactical_options_majority_table(
    #         TVA.determine_tactical_options(
    #             VotingScheme.borda_count, HappinessScheme.borda_count
    #         )
    #     ))
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
    parser.add_argument(
        "--candidates-count", type=int, default=5, required=False
    )
    parser.add_argument(
        "--distribution-type",
        type=str,
        choices=tuple(h.name for h in DistributionTypes),
        default="uniform",
        required=False,
        help="The distribution from which the voters preferences will be sampled",
    )
    parser.add_argument("--voters-count", type=int, default=10, required=False)
    parser.add_argument(
        "--happiness-scheme",
        choices=tuple(h.name for h in HappinessScheme),
        default="cubed_weight",
    )
    parser.add_argument(
        "--voting-scheme",
        choices=tuple(h.name for h in VotingScheme),
        default="borda_count",
    )
    args = parser.parse_args()
    import json

    print("Arguments used:")
    print(json.dumps(args.__dict__, indent=4), "\n")
    assert (
        0 < args.candidates_count < 8
    ), "ERROR: Candidates count must be between 0 and 8"
    main(
        args.candidates_count,
        args.voters_count,
        args.distribution_type,
        happiness_scheme_name=args.happiness_scheme,
        voting_scheme_name=args.voting_scheme,
    )
