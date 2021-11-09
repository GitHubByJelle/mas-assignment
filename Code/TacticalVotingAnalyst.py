from VotingSituation import *
from VotingSchemes import *
import collections


class TacticalVotingAnalyst:
    def __init__(self, candidates, voters):
        """
        Initialisation
        :param candidates: list of objects from class 'Candidate'
        :param voters: list of objects from class 'Voter'
        """
        self.voting_situation = VotingSituation(candidates, voters)
        self.voting_schemes_dict = self.create_voting_vectors(len(candidates))
        self.outcome = {}

    def create_voting_vectors(self, num_candidates):
        """
        Create vectors for different voting schemes
        :param num_candidates: Number of candidates
        :return: Dictionary with vectors for several voting schemes
        """
        return {
            "plurality": create_vote_for_n_vector(1, num_candidates),
            "vote for 2": create_vote_for_n_vector(2, num_candidates),
            "borda count": create_borda_count(num_candidates),
            "anti plurality": create_vote_for_n_vector(
                num_candidates - 1, num_candidates
            ),
        }

    def get_winner(self, voting_scheme, print_winner=False):
        """
        Determine the winner according to a specific voting scheme
        :param voting_scheme: String of which voting scheme to use
        :param print_winner: bool that indicates if the results from this voting scheme should be printed
        :return: The name (string) of the candidate that won according to the specified voting scheme
        """
        # Create a counter for every candidate
        counter = self.create_count_dict()

        # For every voter
        for voter in self.voting_situation.voters:
            # Process all preferences
            for i in range(len(voter.tactical_preferences)):
                # Add score to the counter dictionary
                counter[voter.tactical_preferences[i].name] += self.voting_schemes_dict[
                    voting_scheme
                ][i]

        # If the user wants to print results
        if print_winner:
            # Print voting scheme
            print("Voting Scheme - {}:".format(voting_scheme))
            i = 1
            # Print sorted results (based on decreasing votes)
            for k, v in sorted(counter.items(), key=lambda x: x[1], reverse=True):
                print("{}) {}: {}".format(i, k, v))
                i += 1
            print()

        # Return the name of the best scoring candidate
        return max(counter, key=counter.get), counter

    def get_winners(self):
        """
        Determine the winner for all different voting schemes
        :return: Dictionary with the name of each candidate that won
        """

        # Create empty dictionary
        winners = {}

        # For every voting scheme, determine the winner
        for voting_scheme in self.voting_schemes_dict.keys():
            winner, counter = self.get_winner(voting_scheme)
            winners[voting_scheme] = winner
            self.outcome[voting_scheme] = collections.OrderedDict(
                dict(sorted(counter.items(), reverse=True, key=lambda item: item[1]))
            )

        # Return the winner
        return winners

    def create_count_dict(self):
        """
        Create a dictionary for every candidate with value 0 (for counting)
        :return: A dictionary for every candidate with value 0 (for counting)
        """
        counter = {}
        for candidate in self.voting_situation.candidates:
            counter[candidate.name] = 0
        return counter

    def overall_happiness(self):
        """
        Determine the overall happiness for each of the voting schemes
        """
        overall_happiness = {}
        for voting_scheme in self.voting_schemes_dict.keys():
            happiness = 0
            for voter in self.voting_situation.voters:
                happiness += voter.determine_happiness(self.outcome[voting_scheme])
            overall_happiness[voting_scheme] = happiness

        return overall_happiness
