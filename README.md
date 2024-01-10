# APININE FOLDER STRUCTURE

In this repository, we propose a folder structure for our API service.
The code organized in multiple levels.
The top level folders are the following:

    - **src** : contains the application code with the necessary requirements and configurations (Makefile, Dockerfile)
    - **infra**: contains the IaC code (terraform)
    - **.vscode**: contains the VSC editor configurations
    - **.github/wokrflows**: contains the definitions of the github workflows (pipelines)

## SRC
Each folder in **src** represents a specific risk assessemnt endpoint (wildifire, flood) with exception of the folder *common* which is a module containing shared utilities functions.
Within each directory, one can find:

    - **.py* files: application code
    - *test* folder: contains pytest tests
    - *Dockerfile*: used to build the Docker image to be used in Lambda functions
    - *Makefile*: automates common actions (build, tests, etc..)

*Makefile* and *Dockerfile* are not present in the *common* folder -> TO BE VERIFIED

Every Dockerfile uses the parent context (src) instead of the current folder (src/wildfire) to solve import
issues between folders. The other option was to copy the common folder inside the current directory, build the container image and then delete the copied folder. This solution could lead to unclean situation that lead to unexpected behaviours and committing multiple copies of *common*.
The Makefile inside each directory moves to the src parent folder before building the container.
*pytest.ini* is necessary because it updates the PYTHONPATH for pytests, adding *src* (..).

## .vscode
The only important configuration is *terminal.integrated.env.linux* that injects custom environment variable in VSC shell.
We set it to update the PYTHONPATH, so that the code inside every risk folder can import common folder.

## .github/workflows
Each application folder trigger a build only when the code inside that specific folder **or in common**  is updated.

TODO: write a workflow for each risk and infra.