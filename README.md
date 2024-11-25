# This repo tests the analysis files from the forked repo \
-The "test" branch is our final branch which contains all of the test files.
### Running the test
Use:
python -m coverage run -m unittest discover
To view the coverage results use the following:
python -m coverage report --omit=test*
The results of our testing produced 94% overall coverage
Stretching over 589 statements and only having 34 misses
# ENPM611 Project Application Template

This is the template for the ENPM611 class project. Use this template in conjunction with the provided data to implement an application that analyzes GitHub issues for the [poetry](https://github.com/python-poetry/poetry/issues) Open Source project and generates interesting insights.

This application template implements some of the basic functions:

- `data_loader.py`: Utility to load the issues from the provided data file and returns the issues in a runtime data structure (e.g., objects)
- `model.py`: Implements the data model into which the data file is loaded. The data can then be accessed by accessing the fields of objects.
- `config.py`: Supports configuring the application via the `config.json` file. You can add other configuration paramters to the `config.json` file.
- `run.py`: This is the module that will be invoked to run your application. Based on the `--feature` command line parameter, one of the three analyses you implemented will be run. You need to extend this module to call other analyses.

With the utility functions provided, you should focus on implementing creative analyses that generate intersting and insightful insights.

In addition to the utility functions, an example analysis has also been implemented in `example_analysis.py`. It illustrates how to use the provided utility functions and how to produce output.clear

## Setup

To get started, your team should create a fork of this repository. Then, every team member should clone your repository to their local computer. 


### Install dependencies

In the root directory of the application, create a virtual environment, activate that environment, and install the dependencies like so:

```
pip install -r requirements.txt
```

### Download and configure the data file

Download the data file (in `json` format) from the project assignment in Canvas and update the `config.json` with the path to the file. Note, you can also specify an environment variable by the same name as the config setting (`ENPM611_PROJECT_DATA_PATH`) to avoid committing your personal path to the repository.


### Run an analysis

With everything set up, you should be able to run the existing example analysis:

```
python run.py --feature 0
```

That will output basic information about the issues to the command line.

## VSCode run configuration

To make the application easier to debug, runtime configurations are provided to run each of the analyses you are implementing. When you click on the run button in the left-hand side toolbar, you can select to run one of the three analyses or run the file you are currently viewing. That makes debugging a little easier. This run configuration is specified in the `.vscode/launch.json` if you want to modify it.

The `.vscode/settings.json` also customizes the VSCode user interface sligthly to make navigation and debugging easier. But that is a matter of preference and can be turned off by removing the appropriate settings.

# GitHub Issues Analysis for the Poetry Project

Each analysis script can be executed via the command line using the run.py orchestrator module. Below are instructions for running each of the three analyses.

## 1. Issue Analysis: Time taken to assign a user to an issue
Module: issue_analysis.py

Description: This module provides an analysis of the issue management process, offering an overview of open and closed issues, the number of issues assigned to users, and the time it takes to assign a user to an issue.

How to Run:

```
python run.py --feature 1
```

To check how long it takes to assign a user to a specific label, run the following command:

```
python run.py --feature 1 --label <labelname>
```

Replace <labelname> with the specfic label you wish to analyze.

## 2. Time Based Issue Analysis
Module: time_based_issue_analysis.py

Description: Provides insights like the longest amount of time taken by a user to close an issue [i] and also a graph about how long it takes a specific user to close an issue, segregated label-wise [ii]. 

How to Run:

```
[i] python run.py --feature 2
[ii] python run.py --feature 2 --user <username>
```

Replace <username> with the GitHub username you wish to analyze.

Example:

```
[i] python run.py --feature 2
[ii] python run.py --feature 2 --user TheButlah
```

## 3. Reopened Issue Analysis
Module: reopened_issue_analysis.py

Description: This analysis prioritizes gaining insights by understanding the characteristics and patterns of GitHub issues that were closed and then later reopened. It brings back useful data on the quality and effectiveness of issue resolution, to indicate whether initial fixes were effective or if there was a requirement to reopen the issue to work on the resolution further sometime later post closure.

How to Run: 
```
python run.py --feature 3 
```

## 4. User-Specific Issue Analysis
Module: user_specific_issue_analysis.py

Description: Provides insights into a specific user's interactions with issues having different event labels like CLI, Triage, Bug etc. 

How to Run:

```
python run.py --feature 4 --user <username>
```

Replace <username> with the GitHub username you wish to analyze.

Example:

```
python run.py --feature 4 --user finswimmer
```

## 5. Label Trend Analysis
Module: label_trend_analysis.py

Description: Analyzes the trend of label usage over time for the top 5 most frequently used labels.

How to Run:

```
python run.py --feature 5
```

## 6. Event Label Categories Analysis
Module: event_label_categories_analysis.py

Description: Counts the number of label-related events based on specified label categories (e.g., status/, area/). Allows dynamic analysis based on the label prefix provided.

How to Run:

```
python run.py --feature 6 --label status
```
This command analyzes labels that start with status/ (e.g., status/triage, status/wontfix).

Note: Replace status with any other label prefix as needed.
