# Contributing

# Development Quickstart


Create a virtual environment and install `ananke` in this environment for running.
```{bash}
git clone git@gitlab.com:causal/ananke.git

cd ananke

python3 -m venv env

source env/bin/activate # this activates your environment

pip3 install -e .
```

Make sure that there are no `.egg_info` folders (will not be an issue cloning from gitlab) as these can mess up installation.

It is also necessary to install separate development python packages:
```{bash}
pip3 install -r dev_requirements.txt
```

as well as separate system packages: 

- Building the sphinx-notebook support:
```{bash}
# this will depend on your environment, e.g.
sudo apt install pandoc # ubuntu
sudo dnf install pandoc # fedora
```

- graphviz (see [README.md](README.md))


Now you are ready to develop!


# Developing Notes 
## Running Tests
To run tests locally (within the virtual environment):
```{bash}
python3 -m pytest tests/ # all tests

python3 -m pytest tests/graphs/test_admg.py # all tests in admg.py

python3 -m pytest tests/graphs/test_admg.py::TestADMG # a particular TestCase in admg.py

python3 -m pytest tests/graphs/test_admg.py::TestADMG::test_obtaining_districts # a particular TestCase method in admg.py
```

Continuous integration has been set up to run tests on pushes to the `master` branch.

## Adding Requirements

Python packages that are required for development purposes but not for production purposes (e.g. `pytest`) should be placed into `dev_requirements.txt`. Python packages that are required for both development and production purposes should be added to the `requirement` list in `setup.py`.

Non-Python packages should be separately added to the CI configuration in `.gitlab.ci.yml` as well as `tox.ini`, and a note on how to install this non-Python package added to the documentation in `docs`.

## Before Pushing 
Consider using the following command to lint the code

`flake8 ananke/`


## Test Coverage

```{bash}
pytest --cov=ananke tests/  # to generate the base report

```

## Running tests through tox
Tox runs tests as if they were installed from the pypi repository. Run `tox` in the project root to run the pytest tests in a virtualenv with ananke installed as a non-editable package.

## Development Git pattern

Ideally the cycle should work like this:

* An issue is created requesting a feature or a bugfix
* Create branch from `dev` (e.g. `mybranch`) and make changes
* Push changes to `mybranch`
## Building docs

* To build docs, run `bash run.sh` from the `docs` folder.
* Add tutorial notebooks in `docs/notebooks`. These are automatically built into webpages.
* Maintain a `references.bib` in `docs/source`. 

## How to update the pypi repository
* Switch to `dev` branch
* Increment the version number accordingly in `setup.py`
* Commit this file with message `v*.*.*` as appropriate
* Tag the gitlab release with the new version number using `git tag -a v*.*.* -m "v*.*.*"`
* Push `dev` to `origin`
* Merge `dev` to `master` on gitlab
* Run `python setup.py bdist_wheel`
* Upload the wheel using `twine upload dist/*`

