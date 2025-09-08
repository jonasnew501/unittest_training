## About this project
The purpose of this project is to practice the usage of unittests with the library "pytest" in Python.

Also, the conduction of CI ('Continuous Integration') via GitHub Actions, i.e. the automated execution
of the unittests on certain actions (e.g. with every push to the remote repository) via a YAML-file
is practiced.



## What I Learned
- **Why, when executing `pytest` from the root directory (in this project `unittest_training`),  
  the imports from files inside `src/` into a file inside `tests/` often fail — and how to solve it.**

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

  <br>

- **How to properly structure and format function docstrings**

  <br>

- **Raising domain-specific custom Exceptions instead of built-in Exceptions is a practice of clean code.**  
    - By doing that, implementation-details are hidden from the caller; they don´t need to know or reason about  
      how the respective function was implemented (based off of an Exception it threw).
  
    - Furthermore, using domain-specific custom Exceptions makes code-maintainance more easy, because when refactoring  
      for example, it is more unlikely that the exceptions used in the accompanying unit-tests need to be changed / adapted  
      too if domain-specific custom Exceptions are used compared to when built-in, very specific exceptions are used.

  <br>

- **How pytest handles the context-manager 'with pytest.raises([SomeException])'**
    - When using the context-manager 'with pytest.raises([SomeException]'), only one function which is expected to raise  
      this exception must be contained in that context-manager.  
      *-->Reason:* As soon as a function in that context-manager actually raises the specified exception, the context-manager    
      is exited immediately. Thus all other code that comes below that function which rose the specified exception is dead code.

      -->As a consequence, per context-manager with 'with pytest.raises([SomeException])' only one function, which is expected
      to raise 'SomeException' must be contained.

- XXX