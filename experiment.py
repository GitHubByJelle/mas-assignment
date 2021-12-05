import numpy as np
from enum import Enum
from tactical_voting_analyst.voter import Voter
import matplotlib.pyplot as plt
import random


class ExperimentType(Enum):
    SIMPLE = 1
    INCREASE_CANDIDATES = 2
    INCREASE_VOTERS = 3


class Experiment:
    def __init__(self, exp_type: ExperimentType, **kwargs):
        self.exp_path = kwargs.get("exp_path", None)
        self.exp_type = exp_type
        self.candidates_names = kwargs.get("candidates_names", None)
        self.candidates = kwargs.get("candidates", None)
        self.preferences = kwargs.get("preferences", None)
        # self.voters = kwargs.get('voters', None)
        self.TVA = kwargs.get("TVA", None)
        self.voting_schemes = kwargs.get("voting_schemes", None)
        self.happiness_scheme = kwargs.get("happiness_scheme", None)
        self.tactical_strategy = kwargs.get("tactical_strategy", None)
        self.risk_type = kwargs.get("risk_type", None)

    def run(self):
        if self.exp_type == ExperimentType.SIMPLE:
            self.run_simple_experiment()
        elif self.exp_type == ExperimentType.INCREASE_CANDIDATES:
            self.run_candidates_experiment()
        elif self.exp_type == ExperimentType.INCREASE_VOTERS:
            self.run_voters_experiment()
        else:
            pass

    def run_simple_experiment(self):
        # self.voters = [Voter(preference) for preference in self.preferences]
        self.tva = self.TVA(
            self.candidates, self.candidates_names, self.preferences
        )
        ax = self.create_ax()
        schemes_happiness_risk = []
        for vs in self.voting_schemes:
            scheme_risk, scheme_happiness = self.get_risk_and_happiness(vs)
            schemes_happiness_risk.append((scheme_happiness, scheme_risk, vs))
            ax.scatter(
                self.apply_jitter(scheme_risk),
                scheme_happiness,
                label=str(vs.__repr__())[14:].split(":")[0],
                alpha=0.7,
            )

        self.format_ax(ax)
        plt.savefig(self.exp_path + "/results.png")

    def run_candidates_experiment(self):
        ax = self.create_ax()
        schemes_happiness_risk = {}
        for i, cnames in enumerate(self.candidates_names):
            self.tva = self.TVA(
                self.candidates[i], cnames, self.preferences[i])
            for vs in self.voting_schemes:
                vs_string = str(vs.__repr__())[14:].split(":")[0]
                scheme_risk, scheme_happiness = self.get_risk_and_happiness(vs)
                if vs_string not in schemes_happiness_risk:
                    schemes_happiness_risk[vs_string] = []
                else:
                    schemes_happiness_risk[vs_string].append(
                        (
                            (scheme_happiness, scheme_risk),
                            f"{len(cnames)}",
                        )
                    )

        all_x_points = []
        all_y_points = []
        all_annots = []
        for vs in schemes_happiness_risk:
            print(vs, schemes_happiness_risk[vs])
            ys, xs = list(
                zip(*[vs_n[0] for vs_n in schemes_happiness_risk[vs]])
            )
            xs = self.apply_jitter(xs, multi=True)
            all_x_points += xs
            all_y_points += ys
            annots = [vs_n[1] for vs_n in schemes_happiness_risk[vs]]
            all_annots += annots
            ax.scatter(xs,
                       ys, label=vs, alpha=0.7)

        for i, txt in enumerate(all_annots):
            ax.annotate(txt, (all_x_points[i], all_y_points[i]))

        self.format_ax(ax)
        plt.savefig(self.exp_path + "/results.png")

    def run_voters_experiment(self):
        ax = self.create_ax()
        schemes_happiness_risk = {}
        for i, voters in enumerate(self.preferences):
            self.tva = self.TVA(
                self.candidates, self.candidates_names, self.preferences[i]
            )
            for vs in self.voting_schemes:
                vs_string = str(vs.__repr__())[14:].split(":")[0]
                scheme_risk, scheme_happiness = self.get_risk_and_happiness(vs)
                if vs_string not in schemes_happiness_risk:
                    schemes_happiness_risk[vs_string] = []
                else:
                    schemes_happiness_risk[vs_string].append(
                        (
                            (scheme_happiness, scheme_risk),
                            f"{voters.shape[0]}",
                        )
                    )

        all_x_points = []
        all_y_points = []
        all_annots = []
        for vs in schemes_happiness_risk:
            print(vs, schemes_happiness_risk[vs])
            ys, xs = list(
                zip(*[vs_n[0] for vs_n in schemes_happiness_risk[vs]])
            )
            xs = self.apply_jitter(xs, multi=True)
            all_x_points += xs
            all_y_points += ys
            annots = [vs_n[1] for vs_n in schemes_happiness_risk[vs]]
            all_annots += annots
            ax.scatter(xs,
                       ys, label=vs, alpha=0.7)

        for i, txt in enumerate(all_annots):
            ax.annotate(txt, (all_x_points[i], all_y_points[i]))

        self.format_ax(ax)
        plt.savefig(self.exp_path + "/results.png")

    def get_risk_and_happiness(self, vs):
        if self.tactical_strategy == 'PAIRED':
            scheme_tactical_options = self.tva.determine_paired_tactical_options(
                vs, self.happiness_scheme
            )
        elif self.tactical_strategy == 'RUN-OFF':
            scheme_tactical_options = self.tva.determine_tactical_options_run_off_election(
                self.happiness_scheme
            )
        elif self.tactical_strategy == 'BASIC':
            scheme_tactical_options = self.tva.determine_tactical_options(
                vs, self.happiness_scheme
            )
        else:
            raise Exception('Invalid tactical strategy')
        # print('=======', vs, scheme_tactical_options)
        # _, _, _, new_outcome = scheme_tactical_options[0]
        scheme_risk = self.tva.calculate_risk(
            scheme_tactical_options, vs, self.happiness_scheme, version=self.risk_type)
        scheme_happiness = self.tva.overall_happiness(vs)

        return scheme_risk, scheme_happiness

    def create_ax(self):
        fig = plt.figure()
        ax = plt.subplot(111)
        box = ax.get_position()
        ax.set_position([box.x0, box.y0, box.width * 0.8, box.height])
        return ax

    def format_ax(self, ax):
        ax.set_xlim((0, 1))
        ax.set_ylim((0, 1))
        ax.legend(loc="center left", bbox_to_anchor=(1, 0.5))
        plt.xlabel("Risk")
        plt.ylabel("Happiness")

    def apply_jitter(self, points, multi=False):
        if multi:
            return [p + random.uniform(0.02, 0.05) for p in points]
        else:
            return points + random.uniform(0.01, 0.05)
