## About this project
The purpose of this project is to practice the usage of unittests with the library "pytest" in Python.

Also, the conduction of CI ('Continuous Integration') via GitHub Actions, i.e. the automated execution
of the unittests on certain actions (e.g. with every push to the remote repository) via a YAML-file
is practiced.



## What I Learned
- Why, when executing `pytest` from the root directory (in this project `unittest_training`),  
  the imports from files inside `src/` into a file inside `tests/` often fail — and how to solve it.

  ### ➡️ Why imports failed
  By default, when running `pytest` from the project root, Python does not know that the `src/`  
  directory should be treated as the root for imports.  

  As a result, doing:
  ```python
  from src.calculator import Calculator
  ```
  raised
  ```
  ModuleNotFoundError: No module named 'src'
  ```

  ### ✅ Solution with pyproject.toml
  We configure pytest to add src/ to Python’s import path by adding this to pyproject.toml:
  ```toml
  [tool.pytest.ini_options]
  pythonpath = ["src"]
  ```
  This way, modules inside src/ become importable as top-level packages.
  For example, src/calculator.py can be imported simply as:
  ```
  from calculator import Calculator
  ```

- XXX
