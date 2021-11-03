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
    def determine_happiness(self, counter, type='borda'):
        """
        Determine self happiness
        :param counter: OrderedDict of candidates
        """
        happiness = 0
        if type == 'borda':
            borda = [3, 2, 1, 0]
            for i, candidate in enumerate(self.tactical_preferences):
                happiness += borda[i] * borda[list(counter.keys()).index(candidate.name)]

        return happiness
