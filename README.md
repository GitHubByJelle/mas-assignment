# MAS Assignment

## Requirements:

Notice python version >= 3.9 is required.
The easies way to run this project is to use conda. If you have conda already installed on your system you can run:
``` bash
conda create --name tactical_voting_analyst --file conda_env.txt
conda activate tactical_voting_analyst
```
Alternatively, with pip (less secure):
```
pip install -r pip_env.txt
```
## Running From the Command Line

With the terminal navigate outside the folder `tactical_voting_analyst`. 
The default output will show voters tactical options and can be run by:

``` bash
python -m tactical_voting_analyst
```
Or, to show the help with some options:
``` bash
python -m tactical_voting_analyst -h
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
