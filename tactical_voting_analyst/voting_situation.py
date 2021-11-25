import numpy as np
from pyvis.network import Network


class VotingSituation: # TODO: do we really need this class?
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

    def get_all_preferences(self):
        """
        Get all preferences from all voters
        :return: Return list of tuples with preferences of voters
        """
        preferences = []
        for voter in self.voters:
            preferences.append(tuple(voter.true_preferences))

        return preferences

    def determine_majority_table(self):
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
            for i in range(num_cand-1):
                for j in range(i+1,num_cand):
                    counts[preference[i], preference[j]] += 1

        return counts

    def create_majority_graph_preferences(self, majority_table, file_name = "majority_graph"):
        """
        Create a html file for the visualisation of the majority graph
        :param majority_table: Table with majority values
        :param file_name: File name for the html file
        :return: html file with visualisation of the network
        """
        # Create net
        net = Network(directed=True)
        net.set_edge_smooth('continuous')

        # Create nodes
        num_cand = len(self.candidate_names)
        for c in range(num_cand):
            net.add_node(c, label="{}".format(c+1))

        # Create edges
        for i in range(num_cand-1):
            for j in range(i+1, num_cand):
                if majority_table[i,j] > majority_table[j,i]:
                    net.add_edge(i, j)
                else:
                    net.add_edge(j, i)

        # Set options and show / save
        net.set_options("""var options = {
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
        }""")
        net.show('{}.html'.format(file_name))
