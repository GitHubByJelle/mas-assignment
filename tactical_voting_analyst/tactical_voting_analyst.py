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
        verbose=True,
    ):
        """
        Initialisation
        :param candidates: ndarray of objects from class 'Candidate' np.ndarray[5, np.int_]
        :param voters: list[Voter]
        """
        self.print = Logger(verbose)
        unique_preferences = tuple(set(preferences))
        self.__voter_multipliers = {
            preference: preferences.count(preference)
            for preference in unique_preferences
        }
        voters = [Voter(np.array(preference)) for preference in unique_preferences]
        self.voting_situation = VotingSituation(candidates, candidate_names, voters)
        self.voting_schemes_vectors = self.__create_voting_vectors(len(candidates))

    def __create_voting_vectors(self, num_candidates: int) -> np.ndarray:
        """
        Create vectors for different voting schemes
        :param num_candidates: Number of candidates
        :return: Dictionary with vectors for several voting schemes
        """
        named_voting_vectors = {
            VotingScheme.plurality: create_vote_for_n_vector(1, num_candidates),
            VotingScheme.vote_for_two: create_vote_for_n_vector(2, num_candidates),
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
                voting_scheme * self.__voter_multipliers[tuple(voter.true_preferences)]
            )

            # for i in range(len(voter.true_preferences[0])):
            #     # Add score to the counter dictionary
            #     counter[voter.true_preferences[0][i]] += voting_scheme[i]

        # print(counter)

        # If the user wants to print results
        # Todo: numpy-ize code bellow: DONE
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
            (len(self.voting_schemes_vectors), len(self.voting_situation.candidates),)
        )

        # For every voting scheme, determine the ranked list of candidates
        for i, voting_scheme in enumerate(self.voting_schemes_vectors):
            winners[i] = np.argsort(self.get_winner(voting_scheme))

        # Return the ranked_candidates
        return winners

    def overall_happiness(self, voting_scheme: VotingScheme):
        return self.__overall_happiness(self.voting_schemes_vectors[voting_scheme])

    def __overall_happiness(
        self, voting_scheme: np.ndarray
    ):  # by Giulio: I made it private to ease usage
        """
        Determine the overall happiness for each of the voting schemes
        """
        # ToDO: find most efficient way to do this
        # ranked_candidates_id = np.argsort(-self.get_winner(voting_scheme))
        ranked_candidates_id = np.argsort(-self.get_winner(voting_scheme))

        return sum(  # TODO (by Giulio): consider using average rather than sum
            voter.determine_happiness(ranked_candidates_id)
            * (self.__voter_multipliers[tuple(voter.true_preferences)])
            for voter in self.voting_situation.voters
        ) / len(self.voting_situation.voters)

    def determine_tactical_options(
        self, voting_scheme: VotingScheme, happiness_scheme: HappinessScheme,
    ):
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
                                    self.voting_situation.candidate_names[pref[0]]
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
        self.print("Current outcome: {}\n".format(self.__create_outcome_str(outcome)))

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
                    voting_scheme,
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
                        voting_scheme,
                        happiness_scheme,
                    )
                    for voter in sub_voters
                )
                # If happiness is better for ALL voters in the coalition, add
                if np.array(
                    [new_happiness[i] > curr_happiness[i] for i in range(size_pairs)]
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

        ## OLD CODE
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
                        " > ".join(self.voting_situation.candidate_names[pref[0][1]]),
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
                np.core.defchararray.add(self.voting_situation.candidate_names, ": "),
                outcome.astype(np.int32).astype(str),
            )[(-outcome).argsort()]
        )

    def calculate_risk(self, tactical_options: list[tuple]) -> float:
        return len(tuple(to for to in tactical_options if len(to) > 0)) / len(
            tactical_options
        )
        # non_empty_options = 0
        # for voter_tactical_options in tactical_options:
        #    if len(voter_tactical_options) != 0:
        #        non_empty_options += 1
        # return non_empty_options / len(tactical_options)

    def calculate_risk2(
        self, voting_scheme: VotingScheme, happiness_scheme: HappinessScheme
    ):
        tactical_options = self.determine_tactical_options(
            self, voting_scheme, happiness_scheme
        )
        number_candidates = len(self.voting_situation.candidates)
        x = 0
        for voter_tactical_options in tactical_options:
            x += len(voter_tactical_options) / math.factorial(number_candidates)
        risk2 = x / len(tactical_options)
        return risk2

    def calculate_risk3(
        self,
        outcome,
        voting_scheme: VotingScheme,
        happiness_scheme: HappinessScheme,
        tactical_options,
    ):
        print("Outcome is: ", outcome)

        def determine_happiness(outcome):
            return sum(
                voter.determine_happiness(outcome)
                for voter in self.voting_situation.voters
            )

        def x(tactical_option):
            return self.overall_happiness(voting_scheme) - determine_happiness(
                tactical_option
            )

        # outcome = self.get_winner(self.voting_schemes[voting_scheme])
        return sum(x(to) for to in tactical_options) / len(tactical_options)
