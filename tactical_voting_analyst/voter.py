import itertools
# from .candidate import Candidate
import numpy as np

class Voter:
    v_id = 0
    # def __init__(self, preferences: list[list[Candidate]]):
    def __init__(self, preferences: np.ndarray):
        """
        Initialise the preferences of the voter
        :param Preferences: List of objects from class Candidate
        """
        # Make disinction between true preferences and tactical preferences
        # self.true_preferences = preferences[0]
        # self.tactical_options = []
        self.voter_id = Voter.v_id
        Voter.v_id += 1

        self.true_preferences = preferences
        # self._true_preferences_array =
        self.tactical_preferences = preferences

    # Functions that could be created
    def determine_happiness(self, outcome: dict[str, int], voting_scheme : str ="borda"):
        """
        Determine self happiness
        :param outcome: Dict of outcome (based on score, decreased)
        """

        # Sort outcome
        sorted_outcome = [x[0] for x in sorted(outcome.items(), reverse=True, key=lambda item: item[1])]

        # Count happiness
        happiness = 0
        if voting_scheme == "borda count":
            borda = [3, 2, 1, 0]
            for i, candidate in enumerate(self.true_preferences):
                happiness += (
                    borda[i] * borda[sorted_outcome.index(candidate.name)]
                )

        return happiness

    # def update_tactical_options(self, outcome: dict[str, int],  candidates: list[Candidate],
    #                             voting_scheme_dict: dict[str, list[int]], voting_scheme: str = "borda"):
    #     """
    #     Determine the tactical options for each votes
    #     :param outcome: Outcome of the real preferences
    #     :param candidates: List of all candidates
    #     :param voting_scheme_dict: Dictionary of vectors for all voting_schemes
    #     :param voting_scheme: String of selected voting scheme
    #     """
    #     # Reset tactical preferences
    #     self.tactical_options = []
    #
    #     # Determine current happiness
    #     curr_happiness = self.determine_happiness(outcome, voting_scheme)
    #
    #     # Determine outcome without voter
    #     blank_outcome = self.remove_pref_outcome(outcome.copy(), self.true_preferences, voting_scheme_dict[voting_scheme])
    #
    #     # For every permutation of preferences
    #     for perm in list(itertools.permutations(candidates)):
    #         # Determine new outcome
    #         new_outcome = self.add_pref_outcome(blank_outcome.copy(), list(perm), voting_scheme_dict[voting_scheme])
    #
    #         # Calculate new happiness
    #         new_happiness = self.determine_happiness(new_outcome, voting_scheme)
    #
    #         # If it's a better happiness, save
    #         if (new_happiness > curr_happiness):
    #             self.tactical_options.append((list(perm), curr_happiness, new_happiness, new_outcome))
    #
    #     # Sort tactical options based on score
    #     self.tactical_options.sort(key = lambda x: -x[1])
    #
    # def remove_pref_outcome(self, outcome: dict[str, int], preference: list[Candidate],
    #                         voting_scheme_vector: list[int]) -> dict[str, int]:
    #     """
    #     Remove preference from outcome
    #     :param outcome: Current outcome
    #     :param preference: Preference to remove
    #     :param voting_scheme_vector: Lisrt of voting_scheme
    #     :return: Outcome after removing preference
    #     """
    #     # Remove every vote from the outcome
    #     for i in range(len(preference)):
    #         outcome[preference[i].name] -= voting_scheme_vector[i]
    #
    #     # Return outcome
    #     return outcome
    #
    # def add_pref_outcome(self, outcome: dict[str, int], preference: list[Candidate],
    #                         voting_scheme_vector: list[int]) -> dict[str, int]:
    #     """
    #     Add preference to outcome
    #     :param outcome: Current outcome
    #     :param preference: Preference to add
    #     :param voting_scheme_vector: Lisrt of voting_scheme
    #     :return: Outcome after adding preference
    #     """
    #     # Add every vote to the outcome
    #     for i in range(len(preference)):
    #         outcome[preference[i].name] += voting_scheme_vector[i]
    #
    #     # Return outcome
    #     return outcome
