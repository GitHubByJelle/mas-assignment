import sys
import getopt
import os.path
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from tactical_voting_analyst.voter import *


def generate_experiment(argv: list[str]):

    try:
        opts, _ = getopt.getopt(argv,
                                shortopts="",
                                longopts=['exp_folder_name='])

    except getopt.GetoptError as e:
        print('Error: ', e)
        sys.exit(2)

    for opt, arg in opts:
        if opt not in ('--exp_folder_name'):
            print('Invalid parameter')
            sys.exit()
        elif opt == '--exp_folder_name':
            exp_folder = arg
        else:
            print('Invalid parameter')
            sys.exit()

    # Read experiment config file and load variables
    exp_path = './experiments/' + exp_folder
    variables = {}
    exec(open(exp_path + '/config.py').read(), variables)

    candidates_names = variables['CANDIDATES_NAMES']
    candidates = variables['CANDIDATES']
    preferences = variables['PREFERENCES']
    voters = [Voter(np.expand_dims(preference, 0))
              for preference in preferences]
    TVA = variables['TVA'](candidates, candidates_names, voters)
    voting_schemes = variables['VOTING_SCHEMES']
    happiness_scheme = variables['HAPPINESS_SCHEME']

    # Compute happiness and risk for every voting scheme in the experiment
    fig = plt.figure()
    ax = plt.subplot(111)
    box = ax.get_position()
    ax.set_position([box.x0, box.y0, box.width * 0.8, box.height])

    schemes_happiness_risk = []
    for vs in voting_schemes:
        scheme_tactical_options = TVA.determine_tactical_options(
            vs, happiness_scheme)
        scheme_risk = TVA.calculate_risk(scheme_tactical_options)
        scheme_happiness = TVA.overall_happiness(vs)
        schemes_happiness_risk.append((scheme_happiness, scheme_risk))
        print('=====', scheme_happiness, scheme_risk)
        ax.scatter(scheme_risk, scheme_happiness,
                   label=str(vs.__repr__())[14:].split(':')[0], alpha=0.7)

    # ax.xlim((0, 1))
    ax.set_ylim((0, 100))
    ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))
    plt.xlabel('Risk')
    plt.ylabel('Happiness')
    plt.savefig(exp_path + '/results.png')
    # plt.show()


if __name__ == "__main__":
    print(generate_experiment(sys.argv[1:]))
