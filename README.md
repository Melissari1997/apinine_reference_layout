# APININE FOLDER STRUCTURE

In this repository, we propose a folder structure for our API service.
The code organized in multiple levels.

# Motivations
The following structure may look overly complicated, but the idea behind it is simple. 

We want to serve our API using AWS Lambda. Each Lambda has to do **one and one thing only**.

The entrypoint of the Lambda function is the *handler*. For each and every API endpoint, we want a separate handler that knows **which climate scenario** he is dealing with, **which input** to expect and **how to parse environment** variables to retrieve the tiff he has to read.

This leads to a nested structure that separates each case that involves a different combination of these components.

# Structure
The top level folders are the following:

- **src**: contains the application code with the necessary requirements and configurations (Makefile, Dockerfile)
- **infra**: contains the IaC code (terraform)
- **.vscode**: contains the VSC editor configurations
- **.github/workflows**: contains the definitions of the github workflows (pipelines)

Additionally, it contains:
- **.gitignore**
- **.pre-commit-config.yaml**: see [pre-commit](#pre-commit)
- **openapi.yml.tpl**: openapi api template. It is used by terraform to inject the necessary variables and to create the AWS API Gateway deployment.
- **redocly.yaml**: configuration for redocly, the *"Generate beautiful API documentation from OpenAPI"* tool 

## src
The **src** folder contains:
- **api** folder: endpoint code
- **authorizer** folder: lambda custom authorizer
- **generate_store_key** folder: script used for generating API keys. It stores the key both in API Gateway and inside a DynamoDB table. In the future it could be extended to implement key updates, addition or subtraction of specific authorization policies, and more
- **Makefile**: automates common actions (build, tests)

## src/api
Each folder in **src/api** represents a specific risk assessment endpoint (drought, flood, wildfire) with the following exceptions: 
- **common**: folder containing shared utilities functions
- **get_token**: implements /token endpoint redirecting to Cognito OAuth2 endpoints
- **refresh_token**: implements /refresh endpoint redirecting to Cognito OAuth2 endpoints
- **user**: implements /user endpoint, returning logged user's data
- **map**: contains the code for map endpoints,
divided by risk, each of which has a specific folder.

### /src/api/*risk*
Within each risk directory (e.g. */src/api/flood*), and each risk map directory (e.g. */src/api/map/flood*), one can find:

- ***.py** files: application code
- **tests** folder: contains pytest tests
- **pytest.ini**: contains pytest configuration
- **requirements.txt**: contains python requirements
- **/*climate_scenario***: a subdirectory for each climate scenario currently developed for that risk. For example, *flood* has the *baseline* and *rcp* subfolders.

### /src/api/*risk*/*climate-scenario*
Within each climate scenario directory (e.g. */src/api/flood/baseline*), and each climate scenario map directory (e.g. */src/api/map/flood/baseline*), one can find:

- **handler.py**: entrypoint of the lambda function
- **Dockerfile**: used to build the Docker image to be used in Lambda functions
- **build-env-variables.json**: a json containing information to be injected into the docker image, like path of the .tiff files, and, in case of RCP scenarios, the reference year of that .tiff


Every Dockerfile uses the parent context (src) instead of the current folder (src/wildfire) to solve import
issues between folders.

The Makefile inside each directory moves to the src parent folder before building the container.

*pytest.ini* is necessary because it updates the PYTHONPATH for pytests, adding *src* (..).

## Generate Key

It is possible to generate a key from the script in *src/generate_store_key*.
The script will generate an API Gateway Key, hash it and store it on DynamoDB. Additionally it is possible to specify
which API the key is allowed to invoke and in which Organization it belongs to. All these pieces of information are persisted on DynamoDB (the table is created in the *infra* folder).

## .vscode
The only important configuration is *terminal.integrated.env.linux* that injects custom environment variable in VSC shell.
We set it to update the PYTHONPATH, so that the code inside every risk folder can import common folder.

In order to use the integrated test VSCode utility, it's necessary to set the *python.testing.pytestArgs* value to the directory whose tests have to be run (e.g. "src/api/flood")

## .github/actions
Contains the folders of composite actions to be called by workflows. They are:
- **build-push-layout**: automates the docker building, tagging and pushing of images to ECR
- **build-push-layout-map**: automates the docker building, tagging and pushing of images of map endpoints to ECR (to be removed in a future refactoring)
- **terraform-plan**: automates the terraform flow to validate and plan current changes in a certain directory. It also creates a comment on the PR with the computed plan

## .github/workflows
Each application folder trigger a build only when the code inside that specific folder **or in common**  is updated.

Each workflow leverage the reusable workflow *build-test-deploy.yml* that extracts the GEOTIFF_JSON from the *build-env-variables.json* file before calling the *build-push-layout* action. This way each workflow just has to specify a list of variables, like the name of Docker image and Lambda function to be updated.

# Testing

There are two ways to run tests:
1. By running make inside the src folder. The following combinations are supported:
   - ```make testapi```            Run API tests
   - ```make testauthorizer```     Run Lambda Authorizer tests
   - ```make testall```            Run all the tests
2. By using the VSCode extension as explained in the [.vscode subsection](#vscode)

# Code consistency
Code consistency is enforced through the use of [pre-commit](https://pre-commit.com/) and [Ruff](https://docs.astral.sh/ruff/).

## pre-commit
pre-commit is a tool performing a list of checks at commit time. Enforced commits are configured in file *.pre-commit-config.yaml*:
- **default hooks**: performs standard checks
- **ruff**: code linting and automatic fixing
- **black**: code formatting

### pre-commit setup
To install the hooks, run the following command in the root directory:

```
pre-commit install
```

Then, just stage your git changes and commit them in the usual fashion.

When committing the first time, *pre-commit* initializes the hooks and it can take some seconds. After that, the checks are run and, if any are invalidated, commit are stopped and errors are shown.

In case of fixable erros, pre-commit will fix the appropriate files but is still the user's responsibility to check them, stage and commit them again.

## Ruff
Ruff works alongside Black to format the codebase in a clean fashion.

It runs every time a *.py* file is saved and performs, among other things, linting, import sorting, etc. The list of rules we use is present in the pyproject.toml file, under **[tool.ruff.select]** voice.
