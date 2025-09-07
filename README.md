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
  ```python
  from calculator import Calculator
  ```

  <br>

  **However, I then encountered a case where even with a said 'pyproject.toml'-file the 'ModuleNotFoundError' arose.**  
  I then installed the project as described in the following section.

  ### ✅ Solution with 'pip install (-e) [project-name]'
  The project can be installed as a Python package. It can then essentially be imported like other popular Python libraries like "NumPy" or "Pandas".
  
  In order for a project to be installable, the project needs to be structured as a Python package. That means:
    - At least one folder needs to contain an '__init__.py-file, making that folder be treated as a package.
    - Some packaging metadata (the 'pyproject.toml'-file in this project)

  When those two points are met, running 'pip install -e .' from the project-root-directory will create a file  
  inside the 'site-packages'-folder of the python-environment, which points back to the local folder of the project.

  Now, on the machine where this installation was done, the project can be imported from anywhere.  
  Also, local changes of this project are immediately recognized by Python (due to the '-e'-flag, which stands for 'editable mode').  
  This means that no reinstall in necessary once the code in the project is changed.


  After installing the project as a Python package, the import
  ```python
  from calculator import Calculator
  ```
  worked fine when executing 'pytest' in the terminal.

- XXX
