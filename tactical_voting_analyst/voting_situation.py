import numpy as np


class VotingSituation:  # TODO: do we really need this class?
    def __init__(self, candidates, candidate_names: tuple[str, ...], voters):
        """
        Class to store the voting situation
        :param candidates: list of objects from class 'Candidate'
        :param voters: list of objects from class 'Voter'
        """
        self.candidates = candidates
        self.candidate_names = np.array(candidate_names)
        self.voters = voters

    # Functions that could be created
    def add_voter(self):
        pass

    def add_candidate(self):
        pass

    # def get_
