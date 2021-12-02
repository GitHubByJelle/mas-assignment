import numpy as np
from pyvis.network import Network


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

    def get_all_preferences(self) -> list[tuple]:
        """
        Get all preferences from all voters
        :return: Return list of tuples with preferences of voters
        """
        preferences = []
        for voter in self.voters:
            preferences.append(tuple(voter.true_preferences))

        return preferences

    def determine_majority_table(self) -> np.ndarray:
        """
        Create a majority table.
        :return: Returns a majority table, which indicates how many times each candidate won from the
        other candidate looking at simple pairwise majority selection
        """
        # Get all preferences
        preferences = self.get_all_preferences()

        # Determine number of candidates
        num_cand = len(self.candidate_names)

        # Start counting
        counts = np.zeros((num_cand, num_cand))
        for preference in preferences:
            for i in range(num_cand - 1):
                for j in range(i + 1, num_cand):
                    counts[preference[i], preference[j]] += 1

        return counts > counts.T

    def determine_majority_table_pref(self, preferences: list[tuple]) -> np.ndarray:
        """
        Create a majority table.
        :param preferences: The preferences used tp create the majority table
        :return: Returns a majority table, which indicates how many times each candidate won from the
        other candidate looking at simple pairwise majority selection
        """

        # Determine number of candidates
        num_cand = len(self.candidate_names)

        # Start counting
        counts = np.zeros((num_cand, num_cand))
        for preference in preferences:
            for i in range(num_cand - 1):
                for j in range(i + 1, num_cand):
                    counts[preference[i], preference[j]] += 1

        return counts > counts.T

    def create_majority_graph_preferences(
        self, majority_table, file_name="majority_graph"
    ):
        """
        Create a html file for the visualisation of the majority graph
        :param majority_table: Table with majority values
        :param file_name: File name for the html file
        :return: html file with visualisation of the network
        """
        # Create net
        net = Network(directed=True)
        net.set_edge_smooth("continuous")

        # Create nodes
        num_cand = len(self.candidate_names)
        for c in range(num_cand):
            net.add_node(c, label="{}".format(c + 1))

        # Create edges
        for i in range(num_cand - 1):
            for j in range(i + 1, num_cand):
                if majority_table[i, j] > 0:
                    net.add_edge(i, j, width=float(majority_table[i, j]) * 3)
                if majority_table[j, i] > 0:
                    net.add_edge(j, i, width=float(majority_table[j, i]) * 3)

        # Set options and show / save
        net.set_options(
            """var options = {
          "nodes": {
            "color": {
              "border": "rgba(0,0,0,1)",
              "background": "rgba(255,255,255,1)",
              "highlight": {
                "border": "rgba(0,0,0,1)",
                "background": "rgba(208,208,208,1)"
              }
            },
            "font": {
              "strokeWidth": 5
            }
          },
          "edges": {
            "color": {
              "color": "rgba(0,0,0,1)",
              "highlight": "rgba(0,0,0,1)",
              "hover": "rgba(0,0,0,1)",
              "inherit": false
            },
            "smooth": {
              "type": "continuous",
              "forceDirection": "none"
            }
          },
          "physics": {
            "forceAtlas2Based": {
              "gravitationalConstant": -82,
              "centralGravity": 0.015,
              "springLength": 125,
              "springConstant": 0.155,
              "damping": 0.39,
              "avoidOverlap": 0.18
            },
            "maxVelocity": 42,
            "minVelocity": 0.6,
            "solver": "forceAtlas2Based"
          }
        }"""
        )
        net.show("{}.html".format(file_name))

    def get_impact_tactical_options_majority_table(
        self, tactical_options: list[list]
    ) -> np.ndarray:
        """
        How does the majority graph look after tactical voting. This function will return an normalized
        table that relatively indicates in how many cases (if a single voter uses his tactical vote)
        a certain candidate won compared to the other.
        :return: Normalized majority graph
        """
        # Get all preferences
        preferences = self.get_all_preferences()

        # Create one table to keep track of the winning candidates
        majority_table = np.zeros(
            (len(self.candidate_names), len(self.candidate_names))
        )

        # For every voter / vote
        for i in range(len(self.voters)):
            # Get all preferences
            temp_preference = preferences.copy()
            for to in tactical_options[i]:
                # Change the one the voter wants to manipulate
                temp_preference[i] = tuple(to[0])

                # Add the majority table to the big majority table
                majority_table += self.determine_majority_table_pref(temp_preference)

        # Return normalized majority table
        return majority_table / np.sum([len(x) for x in tactical_options])
