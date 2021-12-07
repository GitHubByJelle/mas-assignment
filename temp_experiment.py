from tactical_voting_analyst.init_voters import init_voters, DistributionTypes
from tactical_voting_analyst.tactical_voting_analyst import TacticalVotingAnalyst
import numpy as np
from tactical_voting_analyst.voting_schemes import VotingScheme
from tactical_voting_analyst.happiness_schemes import HappinessScheme

def unfold_preferences(candidates: tuple[str]) -> list[tuple[int, ...]]:
    proto_preferences = tuple(
        v * (tuple(candidates.index(c) for c in p),)
        for p, v in zip(preferences, voter_counts)
    )
    new_preferences: list[tuple[int, ...]] = []
    for ps in proto_preferences:
        new_preferences.extend(ps)

    return new_preferences

candidates_names_lst = [list(map(lambda x: chr(x+65),list(range(n)))) for n in [4, 6, 8]]
voters_count_lst = [7, 35, 70]
distributions = [DistributionTypes.uniform, DistributionTypes.normal, DistributionTypes.two_peaks]
voting_schemes = [VotingScheme.plurality, VotingScheme.anti_plurality, VotingScheme.borda_count]

# For all candidates, voters_count and distributions
for candidates_names in candidates_names_lst:
    for voters_count in voters_count_lst:
        for distribution in distributions:
            for voting_scheme in voting_schemes:
                # Get name of document
                name = "majority_graphs/Cand{}_Vot{}_dist-{}_Scheme-{}".format(len(candidates_names),
                                                     voters_count,
                                                     distribution._name_,
                                                     voting_scheme._name_)

                # Create random preferences
                preferences, voter_counts, observations = init_voters(
                    candidates_names,
                    distribution_function=distribution,
                    voters_count=voters_count,
                    plot=False,
                )

                # Unfold preferences to list[tuple[int]]
                preferences = unfold_preferences(candidates_names)

                # Define candidate int for TVA
                candidates = np.arange(
                        len(candidates_names)
                    )

                # Create TVA (consists of voting situation, needed for analyses
                TVA = TacticalVotingAnalyst(candidates, candidates_names, preferences)

                # Determine the impacted majority table
                impacted_majority_table = TVA.voting_situation.get_impact_tactical_options_majority_table(
                    TVA.determine_tactical_options(
                        VotingScheme.borda_count, HappinessScheme.cubed_weight
                        ))

                # Create a visualisation and save with the correct name
                TVA.voting_situation.create_majority_graph_preferences(impacted_majority_table, file_name=name)
