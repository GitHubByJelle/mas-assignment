from Code.TacticalVotingAnalyst import *
from Code.Candidate import *
from Code.Voter import *

def main():
    # E01.3
    # Set up Candidates
    candidates = [Candidate("A"), Candidate("B"), Candidate("C"), Candidate("D")]

    # Set up Voters
    voters = [Voter([candidates[0], candidates[1], candidates[2], candidates[3]]),
              Voter([candidates[1], candidates[2], candidates[3], candidates[0]]),
              Voter([candidates[2], candidates[3], candidates[0], candidates[1]]),
              Voter([candidates[0], candidates[1], candidates[2], candidates[3]]),
              Voter([candidates[1], candidates[2], candidates[3], candidates[0]]),
              Voter([candidates[2], candidates[3], candidates[0], candidates[1]]),
              Voter([candidates[0], candidates[1], candidates[2], candidates[3]])]

    # Create TVA
    TVA = TacticalVotingAnalyst(candidates, voters)

    print(TVA.get_winners())
    print(TVA.overall_happiness())

    # E01.6
    # Set up Candidates
    candidates = [Candidate("A"), Candidate("B"), Candidate("C")]

    # Set up Voters
    voters = [Voter([candidates[0], candidates[1], candidates[2]]),
              Voter([candidates[0], candidates[1], candidates[2]]),
              Voter([candidates[0], candidates[1], candidates[2]]),
              Voter([candidates[0], candidates[2], candidates[1]]),
              Voter([candidates[0], candidates[2], candidates[1]]),
              Voter([candidates[1], candidates[2], candidates[0]]),
              Voter([candidates[1], candidates[2], candidates[0]]),
              Voter([candidates[2], candidates[1], candidates[0]]),
              Voter([candidates[2], candidates[1], candidates[0]]),
              Voter([candidates[2], candidates[1], candidates[0]]),
              Voter([candidates[2], candidates[1], candidates[0]]),]

    # Create TVA
    TVA = TacticalVotingAnalyst(candidates, voters)

    print(TVA.get_winners())
    print(TVA.overall_happiness())


if __name__ == '__main__':
    main()
