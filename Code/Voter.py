class Voter:
    def __init__(self, Preferences):
        """
        Initialise the preferences of the voter
        :param Preferences: List of objects from class Candidate
        """
        # Make disinction between true preferences and tactical preferences
        self.true_preferences = Preferences
        self.tactical_preferences = Preferences

    # Functions that could be created
    def determine_happiness(self, winner):
        pass
