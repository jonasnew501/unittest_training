## About this project
The purpose of this project is to practice the usage of unittests with the library "pytest" in Python.

Furthermore, the conduction of CI ('Continuous Integration') via GitHub Actions, i.e. the automated execution  
of the unittests on certain actions (e.g. with every push to the remote repository) via YAML-files  
is practiced.

Building an executable is also done/practiced here.


## Structure of this project
### Content
This project consists of four 'Sub'-projects, which are all unrelated to each other.  
These Sub-Projects are:
 - **Basics**: In this sub-project, the basics of writing simple test-cases via Pytest is practiced in the context of a calculator-application.
 - **Fixtures**: The concept of 'fixtures' is practiced in the context of a simple user-manager 'database'.
 - **Mocking**: The concept of 'mocking' is practiced in the context of a calculator-application. The most relevant mocking-functions and -attributes of pytest-mock are listed.
 - **projects/textfile_writer**: The sub-project 'Textfile_writer' - unlike the other three projects - represents a complete, ready-to-use program.  
 This program makes it possible to create a .txt-file and write some text to it, conducts a rollback in case of failure, and conducts a cleanup of the process in all cases.  

 The Sub-project **Textfile_writer** is the most extensive of the four sub-projects.  
 For more information on this sub-project see it´s README under 'src/unittest_training/projects/textfile_writer'.  

 The folder **'github'** contains yaml-files for *actions* and *workflows* on ***GitHub Actions***.  


### Folder-structure
The folderstructure of this project follows a **src-based structure/-layout**.  
The general structure looks like this:
```cpp
project-root/
├── src/
│   └── package-name/
│       ├── __init__.py
│       └── basics/
│       └── fixtures/
│       └── mocking/
│       └── projects/

├── tests/
│       └── basics/
│       └── fixtures/
│       └── mocking/
│       └── projects/
├── dist/
│   └── textfile_writer_cli.exe
├── pyproject.toml
└── README.md
└── requirements.txt
└── .gitignore
└── .github/
```

The 'src'-folder contains the source-code, the 'tests'-folder contains the testing-code.  
As can be seen in the above diagram, for every of the four sub-projects, there is an accompanying folder inside 'tests/'  
containing all the test-code for the respective sub-project.


## Status overview
![Unittests](https://github.com/jonasnew501/unittest_training/actions/workflows/unittests.yml/badge.svg)
![Check for correct code-format](https://github.com/jonasnew501/unittest_training/actions/workflows/formatting_and_linting.yml/badge.svg)

## Tech stack
**Language**  
![Python](https://img.shields.io/badge/Python-3.13-3776AB?logo=python&logoColor=white)  

**Programming Paradigm**  
![OOP](https://img.shields.io/badge/OOP-Object%20Oriented%20Programming-4CAF50)  

**Tools & Workflow**  
![Git](https://img.shields.io/badge/Git-Version%20Control-F05032?logo=git&logoColor=white)  
![GitHub](https://img.shields.io/badge/GitHub-Repos-181717?logo=github&logoColor=white)  

**Testing & CI**  
![PyTest](https://img.shields.io/badge/Testing-PyTest-46375B?logo=pytest&logoColor=white)  
![Pytest-Mock](https://img.shields.io/badge/Testing-Pytest--Mock-6A5ACD?logo=pytest&logoColor=white)  
![GitHub Actions](https://img.shields.io/badge/CI-GitHub%20Actions-2088FF?logo=githubactions&logoColor=white)  

**Packaging & Deployment**  
![PyInstaller](https://img.shields.io/badge/Build%20Tool-PyInstaller-3776AB?logo=python&logoColor=white)  

**Code Formatting**  
![Black](https://img.shields.io/badge/Auto%20Formatting-Black-000000?logo=python&logoColor=white)

**Other Topics Studied**  
![Clean Code](https://img.shields.io/badge/Reading-Clean%20Code-000000)  






## What I Learned
- **Seeing a function as making a 'promise' to / a 'contract' with the caller**
    - A function can be conceptually viewed as making a promise to the caller. It promises:  
      - That potential return-values are correct (e.g. the result of a mathematical operation is correct).  
      - That the datatype of potential return-values are of a specific type/of specific types.  
      - That specific invalid inputs result in specific exceptions the function will raise.  
    
    --> *How this relates to accompanying unit-tests of that function:*  

    The unit-tests are there to test, if all those promises made in the functions´ description (docstring)  
    or in the functions´ name or context it appears in are delivered.  
    The unittests should tests both the 'happy-paths' (as called in Uncle Bobs book 'Clean Code'), i.e.  
    the behavior with valid function input-values, and the 'failure-paths', i.e. the stated function behavior  
    with invalid input-values.  

    After all, the unittests can be seen to prove that the function actually keeps it´s promise (made in its  
    docstring, etc.). Of course this is only true if the unittests are implemented correctly and don´t miss  
    to check a part of the functions´ promise.
  
<br>

- **I learned what the limits of unittests are and what failing unittests actually mean.**
    *Failing unittests show resp. mean that the contract of the related function was broken.*  

    To make this more clear, I will outline a practical example I dived into:  
    - Let´s say there is the function 'divide' (see in 'src/calculator.py' -> class 'Calculator').  
      The function so far makes the promise that it always returns a float for valid inputs.  
      That this promise is delivered is proven by the accompanying unittest, which passes  
      (see in 'tests/test_calculator.py -> class 'TestCalculator' -> function 'test_divide_valid_inputs_correct_datatype').
    - Then, someone wanted to add a new feature to the function 'divide': An integer-division:  
      ```python
      if isinstance(a, int) and isinstance(b, int):
          return a // b #returns an int
      ```
      This would return an integer instead of a float when both input-values of 'divide' are of type 'int'.  
      --> If this feature was added to the functions´ code, the accompanying unittest 'test_divide_valid_inputs_correct_datatype'  
      would of course fail, because the functions promis / contract was broken by adding this new feature.  
      ```python
      #The accompanying unittest:
      @pytest.mark.parametrize(
          "a, b",
          [
              (2, 4), #two positive numbers
              (2, -5), #one positive and one negative number
              (-2.5, -5), #two negative numbers (one is float)
              (0, 0.01), #numerator is zero (denominator is float)
          ]
      )
      def test_divide_valid_inputs_correct_datatype(a, b):
          assert isinstance(Calculator.divide(a, b), float)
      ```
    
    - Now, the question arises how to handle this case:
      - A: The programmer could implement this new feature, adjust the functions´ docstring accordingly and adjust  
           the related unittest 'test_divide_valid_inputs_correct_datatype'.
           --> However, that would mean that the functions´ promise/contract was changed.
      - B: The programmer could leave the function 'divide' as is (maybe rename it to 'divide_floats'), and not implement this new feature in there.  
           Instead, they could create a completely new function for exactly this new feature (e.g. 'divide_integer'),  
           and write accompanying test cases for this new function.  
      
      --> Both approaches have advantages and disadvantages:
      - Approach A has the advantage that potential code-duplication due to creating two very similar functions could be avoided.  
        However, is has the disadvantage that since the contract of the function 'divide' was broken, it is well possible,  
        that other parts of the project, which use 'divide' and rely on 'divide' returning only floats, might now break due to  
        the contract change.  
        ***-->Unit-tests for 'divide' will not capture those potential code-breaks down the line. To detect those potential code-breaks  
        I would argue that other kinds of tests, like integration-tests for example, are necessary, which check if multiple units  
        work together correctly.***  
      - Approach B has the advantage that parts of the code, which rely on the "old" / current contract of 'divide' don´t break potentially,  
        because 'divide' was not changed.  
        However, as already pointed out above, the disadvantage is that code-duplication might happen and thus the maintainability of the  
        codebase might be corrupted by that.  
           
      --> This example showed the limits of unittests.  
      --> Probably in practice in every case an individual decision must be made which approach makes more sense.  

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

- **How pytest handles the context-manager *with pytest.raises([SomeException])***
    - When using the context-manager 'with pytest.raises([SomeException]'), only one function which is expected to raise  
      this exception must be contained in that context-manager.  
      *-->Reason:* As soon as a function in that context-manager actually raises the specified exception, the context-manager    
      is exited immediately. Thus all other code that comes below that function which rose the specified exception is dead code.

      -->As a consequence, per context-manager with 'with pytest.raises([SomeException])' only one function, which is expected
      to raise 'SomeException' must be contained.

<br>

- **How to use pytests´ *parameterize* to avoid code duplication in test-functions**

  Instead of having repeating function-calls resp. 'assert'-statements with just different parameters, like this:
  ```python
  @staticmethod
  def test_divide_valid_inputs():
      assert Calculator.divide(a=2, b=4) == 0.5 #two positive numbers
      assert Calculator.divide(a=2, b=-5) == -0.4 #one positive and one negative number
      assert Calculator.divide(a=-2.5, b=-5) == 0.5 #two negative numbers (one is float)
      assert Calculator.divide(a=0, b=0.01) == 0 #numerator is zero (denominator is float)
  ```

  the test-function can be decorated with the parameters and expected value(s), like so:
  ```python
  @staticmethod
  @pytest.mark.parametrize(
      "a, b, expected",
      [
          (2, 4, 0.5), #two positive numbers
          (2, -5, -0.4), #one positive and one negative number
          (-2.5, -5, 0.5), #two negative numbers (one is float)
          (0, 0.01, 0), #numerator is zero (denominator is float)
      ]
  )
  def test_divide_valid_inputs(a, b, expected):
      assert Calculator.divide(a, b) == expected
  ```

  When using 'pytest.mark.parameterization', pytest creates one separate test case resp. one separate call of the test-function  
  ('test_divide_valid_inputs' in the above example) for every set of parameters.  

  Using test-parameterization makes the test code more readable, maintainable and scalable.  

<br>

- **What *Fixtures* in Pytest are, how to use them, and what their purpose is**

  **Fixtures** in Pytest are reusable, pre-defined functions that provide a reliable setup and teardown for tests.  
  They allow to prepare test data, initialize objects, or configure environments before tests run — and optionally a cleanup after the tests ran is also possible.

  By using fixtures it is possible to:
    - Avoid repetitive setup code
    - Make tests cleaner, modular, and easier to maintain
    - Share common resources across multiple test functions safely

<br>

- **What *Mocking* in Pytest (resp. in *pytest-mock*) is, how to use it, and what its purpose is**

  **Mocking** makes it possible to change the behavior of a specific functionality in the source-code, which is about to be tested.  
  The reason for doing this can be to isolate some functionality of the source-code from external dependencies (e.g. a connection to a database).  
  This isolation is done to limit the testing-scope to that functionality in the source-code, and not extend the testing-scope to the  
  correct functioning of such external dependencies. The latter case would then rather be the scope of *Integration tests* instead of the scope of *Unit tests*.

  Furthermore, mocking can be used to explicitly simulate erroneous behavior of specific functionality, for example a database connection error.  
  By doing that the codes´ behavior in such "unhappy paths" can be tested and corrected when necessary.  

  Additionally, mocking can be used to track/record the call-history of specific functionality.  
  That means a functions´ behavior is not necessarily altered by mocking, but only tracked, and thus afterwards checks such as  
  "Was the function call with the expected argument-values", "Was the function called an expected amount of times", etc. are possible  
  to check the expected behavior of a function/functionality.  

<br>

- **How to build an executable as a CLI (="Command Line Interface") tool**
  
  I used **PyInstaller** in conjunction with Pythons´ **argparse**-module to build a single executable for Windows (i.e. an 'exe'-file)  
  for the *Textfile_writer*-Sub-project described above.  

  This program requires the user to specify two parameters, namely the *text* to write to the txt-file and the *filename* of the txt-file.  
  I decided to build a CLI-tool, that means the executable can only be executed by calling it from a command-line interface (as opposed to double-clicking it),  
  where the user is required to enter the two said parameters.  

  Note:  
  Building and shipping an executable (.exe) is a basic form of software delivery and a good starting point for distributing standalone applications.  
  In professional environments, more advanced delivery approaches are often used — for example, containerization with *Docker*  
  or exposing the application through an API using frameworks like *Flask* or *FastAPI*.  

<br>

- **How to properly create a *requirements.txt*-file**

<br>

- **How and why to structure a Python-project in *src*-layout**

<br>

- **What *__init.py__*-files are and what their purpose is**

<br>

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

