# MAS Assignment

## Requirements:

Notice python version >= 3.9 is required.
The easies way to run this project is to use conda. If you have conda already installed on your system you can run:
``` bash
conda create --name tactical_voting_analyst --file conda_env.txt
conda activate tactical_voting_analyst
```
pip install -r requirements.txt

Run main by:

```
python -m tactical_voting_analyst
```

## Generating a new experiment

To create a new experiment, add a new folder inside `experiments`. Inside it, add a `config.py` file with your experiment parameters. You can copy the `example_experiment` folder and rename it to use as template.

Then, in the root directory, run:

```
python generate_experiment.py --exp_folder_name <your folder name>
```

For instance, taking as example the `example_experiment` folder:

```
python generate_experiment.py --exp_folder_name example_experiment
```
