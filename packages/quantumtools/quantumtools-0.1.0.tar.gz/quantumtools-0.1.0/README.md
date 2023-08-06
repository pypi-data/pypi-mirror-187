# quantum_ml

machine learning utilities

1. Development setup

    1. **Note** prepend `py -3.8 -m` if there are different pythonv versions
    1. Install poetry
        1. `pip install poetry` # develop in python 3.8
    1. **Note** in windows and vscode, need to ensure vscode env path is 
        1. `~/.virtualenvs` 
        1. `"python.venvPath": "~/.virtualenvs"` in settings.json
        1. and `py -3.8 -m poetry config virtualenvs.in-project false`
        1. `py -3.8 -m poetry config virtualenvs.path "~\.virtualenvs"`
    1. to recreate env with updated pyproject.toml
        1. enter python env with `py -3.8 -m poetry shell`
        1. `update_env.bat`
    1. to add dependencies
        1. enter python env `py -3.8 -m poetry shell`
        1. `poetry add packagename@^#.#.#` , @ is for version increase
        1. for development dependencies `poetry add --group dev packagename@^#.#.#` 
    

    
1. Dev Reference
    1. Generate pyproject.toml interactively and create venv
    1. poetry init  or poetry new packagename
    1. Add dependency
        1. poetry add requests # Add --group dev for development dependencies
    1. Install dependencies into venv
        1. poetry install
    1. Activate venv
        1. poetry shell
    1. Exit venv
        1. exit

    1. **NOTE**, to add for installs from github, use `poetry2setup > setup.py`
