# MAS Assignment

Run main by:

```
python -m tactical_voting_analyst
```

## Generating a new experiment

To create a new experiment, add a new folder inside `experiments`. Inside it, add a `config.py` file with your experiment parameters. You can copy the `example_experiment` folder and rename it to use as template.

Then, in the root directory, run:

```
python3 generate_experiment.py --exp_folder_name <your folder name>
```

For instance, taking as example the `example_experiment` folder:

```
python3 generate_experiment.py --exp_folder_name example_experiment
```
