import itertools

from .voting_situation import *
from .voting_schemes import *
from .voter import Voter
from .voting_schemes import VotingScheme
from .happiness_schemes import HappinessScheme
import collections
import numpy as np
import ipdb
import math


class Logger:
    def __init__(self, verbose: bool):
        self.verbose = verbose

    def __call__(self, *msg):
        if self.verbose:
            print(*msg)


class TacticalVotingAnalyst:
    def __init__(
        self,
        candidates: np.ndarray,
        candidate_names: tuple[str, ...],
        preferences: list[tuple[int, ...]],
        *,
        optimize_voters=False,
        verbose=True,
    ):
        """
        Initialisation
        :param candidates: ndarray of objects from class 'Candidate' np.ndarray[5, np.int_]
        :param candidate_names
        :param preferences
        :param optimize_voters: whether to reduces the voters to their unique preferences
        :param verbose: decides if stuff will be printed out (otherwise print will be ignored)
        """
        self.preferences = preferences
        if isinstance(preferences, np.ndarray):
            preferences = tuple(tuple(p) for p in preferences)
        self.print = Logger(verbose)
        unique_preferences = tuple(set(preferences))
        self.__voter_multipliers = {
            preference: preferences.count(preference) if optimize_voters else 1
            for preference in unique_preferences
        }
        voters = [
            Voter(np.array(preference))
            for preference in (
                unique_preferences if optimize_voters else preferences
            )
        ]
        self.voting_situation = VotingSituation(
            candidates, candidate_names, voters
        )
        self.voting_schemes_vectors = self.__create_voting_vectors(
            len(candidates)
        )

    def __create_voting_vectors(self, num_candidates: int) -> np.ndarray:
        """
        Create vectors for different voting schemes
        :param num_candidates: Number of candidates
        :return: Dictionary with vectors for several voting schemes
        """
        named_voting_vectors = {
            VotingScheme.plurality: create_vote_for_n_vector(
                1, num_candidates
            ),
            VotingScheme.vote_for_two: create_vote_for_n_vector(
                2, num_candidates
            ),
            VotingScheme.borda_count: create_borda_count(num_candidates),
            VotingScheme.anti_plurality: create_vote_for_n_vector(
                num_candidates - 1, num_candidates
            ),
        }
        return np.array(
            [
                named_voting_vectors[voting_scheme_name]
                for voting_scheme_name in VotingScheme
            ]
        )

    # def get_winner(self, voting_scheme: str, print_winner = False) ->
    def get_winner(self, voting_scheme: np.ndarray) -> np.ndarray:
        """
        Determine the total number of votes per candidate according to a specific voting scheme
        :param voting_scheme: voting scheme ndarray
        :param print_winner: bool that indicates if the results from this voting scheme should be printed
        :return: ndarray of shape (len(candidates),) containing # votes for each candidate
        """
        # Create a counter for every candidate
        counter = np.zeros(len(self.voting_situation.candidates))

        # For every voter
        for voter in self.voting_situation.voters:
            # Add score to preference of voter
            counter[voter.true_preferences] += (
                voting_scheme
                * self.__voter_multipliers[tuple(voter.true_preferences)]
            )

            # for i in range(len(voter.true_preferences[0])):
            #     # Add score to the counter dictionary
            #     counter[voter.true_preferences[0][i]] += voting_scheme[i]

        # print(counter)

        # If the user wants to print results
        if self.print.verbose:
            # Print voting scheme
            self.print(f"Voting Scheme - {voting_scheme}:")
            sorting = (-counter).copy().argsort()
            for i in sorting:
                self.print(
                    "{}: {}.".format(
                        self.voting_situation.candidate_names[i], counter[i]
                    )
                )

            # i = 1
            # # Print sorted results (based on decreasing votes)
            # for k, v in sorted(counter.items(), key=lambda x: x[1], reverse=True):
            #     print("{}) {}: {}".format(i, k, v))
            #     i += 1
            self.print()

        return counter

    def get_winners(self):
        """
        Determine the ranked_candidates for all different voting schemes
        :return: Dictionary with the name of each candidate that won
        """
        # Create ndarray
        winners = np.zeros(
            (
                len(self.voting_schemes_vectors),
                len(self.voting_situation.candidates),
            )
        )

        # For every voting scheme, determine the ranked list of candidates
        for i, voting_scheme in enumerate(self.voting_schemes_vectors):
            winners[i] = np.argsort(self.get_winner(voting_scheme))

        # Return the ranked_candidates
        return winners

    def overall_happiness(self, voting_scheme: VotingScheme, happiness_scheme: HappinessScheme):
        return self.__overall_happiness(
            self.voting_schemes_vectors[voting_scheme], happiness_scheme
        )

    def __overall_happiness(
        self, voting_scheme: np.ndarray, happiness_scheme: HappinessScheme
    ):  # by Giulio: I made it private to ease usage
        """
        Determine the overall happiness for each of the voting schemes
        """
        # ranked_candidates_id = np.argsort(-self.get_winner(voting_scheme))
        outcome = self.get_winner(voting_scheme)

        return sum(  # TODO (by Giulio): consider using average rather than sum
            voter.determine_happiness(voter.outcome_to_ranked_ids(outcome),
                                      happiness_scheme)
            * (self.__voter_multipliers[tuple(voter.true_preferences)])
            for voter in self.voting_situation.voters
        ) / len(self.voting_situation.voters)

    def determine_tactical_options(
        self, voting_scheme: VotingScheme, happiness_scheme: HappinessScheme,
    ) -> list[list]:
        """
        Determine the tactical voting options for all voters
        :param happiness_scheme: Happiness scheme to calculate happiness
        :param voting_scheme: String of selected voting scheme
        :return: All tactical options
        """
        # Determine outcome
        outcome = self.get_winner(self.voting_schemes_vectors[voting_scheme])

        # Print current outcome
        self.print(f"Current outcome: {self.__create_outcome_str(outcome)}\n")

        # Create list for tactical options
        tactical_options = []

        # For every voter that is in our situation
        for voter in self.voting_situation.voters:
            # Update tactical preference
            voter.update_tactical_options(
                outcome,
                self.voting_schemes_vectors[voting_scheme],
                voting_scheme,
                happiness_scheme,
            )

            # Save tactical options
            tactical_options.append(voter.tactical_options)
            if self.print.verbose:
                print("Voter {}".format(voter.voter_id))
                if len(voter.tactical_options) > 0:
                    for pref in voter.tactical_options:
                        print(
                            "Happiness: {} -> {}, tactical preference: {}, new outcome: {}".format(
                                pref[1],
                                pref[2],
                                " > ".join(
                                    self.voting_situation.candidate_names[
                                        pref[0]
                                    ]
                                ),
                                self.__create_outcome_str(pref[3]),
                            )
                        )
                print()
        """
        print(
            "Risk: ",
            self.calculate_risk3(
                outcome, voting_scheme, happiness_scheme, tactical_options
            ),
        )
        """
        return tactical_options

    def determine_paired_tactical_options(
        self,
        voting_scheme: VotingScheme,
        happiness_scheme: HappinessScheme,
        size_pairs: int = 2,
    ):
        """
        Determine the tactical voting options for all voters when looking in pairs
        :param size_pairs: Size of the pairs in the coalition
        :param happiness_scheme: Happiness scheme to calculate happiness
        :param voting_scheme: String of selected voting scheme
        :return: All tactical options for pairs
        """
        # Determine outcome
        outcome = self.get_winner(self.voting_schemes_vectors[voting_scheme])

        # Print current outcome
        self.print(
            "Current outcome: {}\n".format(self.__create_outcome_str(outcome))
        )

        # Create list for tactical options
        tactical_options = []

        # For every combination of voters (of the given size)
        for comb in itertools.combinations(
            range(len(self.voting_situation.voters)), size_pairs
        ):
            # Create tuple for keeping track of all voters
            sub_voters = tuple(
                self.voting_situation.voters[voter_id] for voter_id in comb
            )

            # Get current happiness for all voters
            curr_happiness = tuple(
                voter.determine_happiness(
                    voter.outcome_to_ranked_ids(outcome),
                    # voting_scheme,
                    happiness_scheme,
                )
                for voter in sub_voters
            )

            # Determine outcome without this voters vote
            blank_outcome = sub_voters[0].remove_pref_outcome(
                outcome,
                sub_voters[0].true_preferences,
                self.voting_schemes_vectors[voting_scheme],
            )
            for voter in sub_voters[1:]:
                blank_outcome = voter.remove_pref_outcome(
                    blank_outcome,
                    voter.true_preferences,
                    self.voting_schemes_vectors[voting_scheme],
                )

            # For every permutation of preferences
            for perm in itertools.permutations(np.arange(len(outcome))):
                # Create an array
                perm = np.array(perm)

                # Determine new outcome by adding voters votes
                new_outcome = sub_voters[0].add_pref_outcome(
                    blank_outcome.copy(),
                    perm,
                    self.voting_schemes_vectors[voting_scheme],
                )
                for voter in sub_voters[1:]:
                    new_outcome = voter.add_pref_outcome(
                        new_outcome.copy(),
                        perm,
                        self.voting_schemes_vectors[voting_scheme],
                    )
                # Determine the new hapiness for all voters
                new_happiness = tuple(
                    voter.determine_happiness(
                        voter.outcome_to_ranked_ids(new_outcome),
                        # voting_scheme,
                        happiness_scheme,
                    )
                    for voter in sub_voters
                )
                # If happiness is better for ALL voters in the coalition, add
                if np.array(
                    [
                        new_happiness[i] > curr_happiness[i]
                        for i in range(size_pairs)
                    ]
                ).all():
                    tactical_option = tuple(
                        (
                            comb[i],
                            perm,
                            curr_happiness[i],
                            new_happiness[i],
                            new_outcome,
                        )
                        for i in range(size_pairs)
                    )
                    tactical_options.append(tactical_option)

        # OLD CODE
        # # For every voter that is in our situation
        # for i in range(len(self.voting_situation.voters) - 1):
        #     # Get voter
        #     voter_one = self.voting_situation.voters[i]
        #
        #     # Determine current happiness
        #     curr_happiness_one = voter_one.determine_happiness(
        #         voter_one.outcome_to_ranked_ids(outcome),
        #         voting_scheme,
        #         happiness_scheme,
        #     )
        #     # Determine outcome without this voter vote
        #     blank_outcome_one = voter_one.remove_pref_outcome(
        #         outcome, voter_one.true_preferences, self.voting_schemes[voting_scheme],
        #         )
        #     # For every voter, voter one could co-op with
        #     for j in range(i+1, len(self.voting_situation.voters)):
        #         # Get voter
        #         voter_two = self.voting_situation.voters[j]
        #
        #         # Determine current happiness
        #         curr_happiness_two = voter_two.determine_happiness(
        #             voter_two.outcome_to_ranked_ids(outcome),
        #             voting_scheme,
        #             happiness_scheme,
        #             )
        #
        #         # Determine outcome without the votes of BOTH voters
        #         blank_outcome = self.voting_situation.voters[j].remove_pref_outcome(
        #             blank_outcome_one, self.voting_situation.voters[j].true_preferences,
        #             self.voting_schemes[voting_scheme],
        #             )
        #
        #         # For every permutation of preferences
        #         for perm in itertools.permutations(np.arange(len(outcome))):
        #             # Create an array
        #             perm = np.array(perm)
        #
        #             # Determine new outcome by adding voters votes
        #             # Voter two
        #             new_outcome = voter_two.add_pref_outcome(
        #                 # Voter one
        #                 voter_one.add_pref_outcome(
        #                     blank_outcome.copy(), perm, self.voting_schemes[voting_scheme],
        #                     ),
        #                 perm,
        #                 self.voting_schemes[voting_scheme],
        #             )
        #
        #             # Calculate new happiness for both voters
        #             new_happiness_one = voter_one.determine_happiness(
        #                 voter_one.outcome_to_ranked_ids(new_outcome),
        #                 voting_scheme,
        #                 happiness_scheme,
        #             )
        #
        #             new_happiness_two = voter_two.determine_happiness(
        #                 voter_two.outcome_to_ranked_ids(new_outcome),
        #                 voting_scheme,
        #                 happiness_scheme,
        #             )
        #
        #             # If it's a better happiness (for BOTH voters), save
        #             if new_happiness_one > curr_happiness_one and new_happiness_two > curr_happiness_two:
        #                 tactical_options.append(((i, perm, curr_happiness_one, new_happiness_one, new_outcome),
        #                                          (j, perm, curr_happiness_two, new_happiness_two, new_outcome)))
        if self.print.verbose:
            # Print outcome
            for pref in tactical_options:
                print(
                    "Voters: {}, Happiness: ({}) -> ({}), tactical preference: {}, new outcome: {}".format(
                        " & ".join([str(x[0]) for x in pref]),
                        ", ".join([str(x[2]) for x in pref]),
                        ", ".join([str(x[3]) for x in pref]),
                        " > ".join(
                            self.voting_situation.candidate_names[pref[0][1]]
                        ),
                        self.__create_outcome_str(pref[0][4]),
                    )
                )

        return tactical_options

    def __create_outcome_str(self, outcome: np.ndarray) -> str:
        """
        Creates a string as output for a given outcome (adding candidate names)
        :param outcome: Social outcome of votings (vector, where each value represents a candidate)
        :return: String with names added
        """
        return ", ".join(
            np.core.defchararray.add(
                np.core.defchararray.add(
                    self.voting_situation.candidate_names, ": "
                ),
                outcome.astype(np.int32).astype(str),
            )[(-outcome).argsort()]
        )

    def calculate_risk(
        self,
        tactical_options: list[tuple],
        voting_scheme: VotingScheme,
        happiness_scheme: HappinessScheme,
        version=0,
    ) -> float:
        risk = 0
        if version == 0:
            risk = len(
                tuple(to for to in tactical_options if len(to) > 0)
            ) / len(tactical_options)
        elif version == 1:
            tactical_options = self.determine_tactical_options(
                voting_scheme, happiness_scheme
            )
            number_candidates = len(self.voting_situation.candidates)
            x = 0
            for voter_tactical_options in tactical_options:
                x += len(voter_tactical_options) / math.factorial(
                    number_candidates
                )
            risk = x / len(tactical_options)
        elif version == 3:

            def determine_happiness(outcome):
                return sum(
                    voter.determine_happiness(voter.outcome_to_ranked_ids(outcome), happiness_scheme)
                    for voter in self.voting_situation.voters
                )

            def x(tactical_option):
                return self.overall_happiness(
                    voting_scheme
                ) - determine_happiness(tactical_option)

            # outcome = self.get_winner(self.voting_schemes[voting_scheme])
            risk = sum(x(to) for to in tactical_options) / len(
                tactical_options
            )

        return risk

    def impact_on_all_other_happiness(
        self, voting_scheme: VotingScheme, happiness_scheme: HappinessScheme
    ):
        """
        Every tactical option (of every voter) has an impact on the final outcome which can be measured by the difference
        between the true overall happiness H and the new overall happiness H': diff = H-H'
        :return: the impact is measured as the average of difference between the new happiness and the true happiness for
        each tactical option (for all voters)
        """

        # determine true happiness H given voting scheme
        true_H = self.overall_happiness(voting_scheme=voting_scheme, happiness_scheme=happiness_scheme)

        # compute tactical options given happiness
        self.determine_tactical_options(voting_scheme=voting_scheme, happiness_scheme=happiness_scheme)

        # For every tactical option we want to measure the difference in happiness
        # ToDo: we should consider creating a unique overall_happines with the option to input an outcome
        def new_overall_H(outcome):
            return sum(
                voter.determine_happiness(voter.outcome_to_ranked_ids(outcome), happiness_scheme)
                * (self.__voter_multipliers[tuple(voter.true_preferences)])
                for voter in self.voting_situation.voters
            ) / len(self.voting_situation.voters)

        diff = 0
        for voter in self.voting_situation.voters:
            pref = voter.tactical_options[0]
            # compute new overall_happiness H' and diff = H' - H
            new_H = new_overall_H(pref[3])
            diff += new_H - true_H

        impact = diff / len(self.voting_situation.voters)
        return impact

    def determine_tactical_options_run_off_election(
        self,
        # preferences: np.ndarray,
        happiness_scheme: HappinessScheme = HappinessScheme.borda_count,
    ) -> list[list[tuple]]:
        """
        Determine tactical options on run off election going over all permutations
        :param preferences: Get all real preferences of all voters
        :param happiness_scheme: Happiness scheme used
        :return: All tactical options
        """
        # Create list for tactical options
        tactical_options = []

        # Get number of voters and candidates
        V = self.preferences.shape[0]
        C = self.preferences.shape[1]

        # For each voter
        for i in range(V):
            # Create a list for the voter
            options_voter = []

            # Determine current happiness
            curr_happiness = self.voting_situation.voters[
                i
            ].determine_happiness(
                self.run_off_outcome_to_ranking(
                    self.perform_run_off_election(self.preferences)
                ),
                happiness_scheme,
            )

            temp_preferences = self.preferences.copy()
            # Look at all permutations
            for perm in itertools.permutations(np.arange(C)):
                # Replace with preference
                temp_preferences[i, ...] = np.array(perm)
                print(temp_preferences)

                # Get outcome of performing run off election
                outcome = self.perform_run_off_election(temp_preferences)

                # Get ranking of candidates
                ranking = self.run_off_outcome_to_ranking(outcome)

                # Calculate happiness
                new_happiness = self.voting_situation.voters[
                    i
                ].determine_happiness(ranking, happiness_scheme)

                if new_happiness > curr_happiness:
                    options_voter.append(
                        (perm, curr_happiness, new_happiness, ranking)
                    )

            # Add to tactical options
            tactical_options.append(options_voter)

        return tactical_options

    def perform_run_off_election(self, preferences: np.ndarray) -> tuple:
        """
        Run off election: Voting is done in two rounds: in the first round each voter casts a single vote
        (“vote for 1”) and the two best candidates are selected, and in the second round the
        winner is determined.
        :param preferences: preferences of all voters
        :return: Outcome round 1, winners round 1, outcome round 2, winner round 2 (winner of election)
        """
        # FIRST ROUND
        # NORMAL VOTING
        # Create a counter for every candidate
        counter = np.zeros(len(self.voting_situation.candidates))

        # For every preference
        for i in range(preferences.shape[0]):
            # Add score to preference
            counter[preferences[i]] += (
                self.voting_schemes_vectors[VotingScheme.plurality]
                * self.__voter_multipliers[
                    tuple(self.voting_situation.voters[i].true_preferences)
                ]
            )

        # Get two winners
        two_winners = (-counter).argsort()[:2].astype(np.int32)

        # ROUND TWO
        # Determine wins for number one and number two (simple majority selection)
        wins_one = (
            np.where(preferences == two_winners[0])[1]
            < np.where(preferences == two_winners[1])[1]
        ).sum()
        wins_two = preferences.shape[0] - wins_one

        # Get winner
        winner = two_winners[0] if wins_one > wins_two else two_winners[1]

        # Return results
        return (counter, two_winners, (wins_one, wins_two), winner)

    def run_off_outcome_to_ranking(self, run_off_outcome: tuple) -> np.ndarray:
        """
        Convert to run off outcome to a ranking of candidates
        :param run_off_outcome:
        :return: ranking of candidates
        """
        # Round one ranked
        ranked = (-run_off_outcome[0]).argsort().astype(np.int32)

        # Round two swapped?
        if run_off_outcome[1][0] != run_off_outcome[3]:
            ranked[0] = run_off_outcome[3]
            ranked[1] = run_off_outcome[1][0]

        return ranked
