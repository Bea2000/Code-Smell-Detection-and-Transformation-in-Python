# Code Smell Detection and Transformation in Python

## Project Overview

This project was completed as part of the **Testing Course** in the second semester of 2022 while studying engineering at **Pontificia Universidad Católica de Chile**. The main goal of the project is to create rules for detecting code smells and implementing code transformation rules for Python programs using static analysis.

The project focuses on automating code quality review processes through the use of **Abstract Syntax Trees (AST)**, a feature provided by Python’s `ast` module. The AST allows for automatic detection of certain code smells and the transformation of Python code to correct or refactor it. The implemented system can automatically review unit tests, detect common code smells, and apply transformations that help auto-repair specific defects.

## Objectives

- Understand the implementation details of static analysis tools.
- Develop custom rules for automatic source code review.
- Implement code transformations that can automatically repair certain types of defects in unit tests.

## Features

### Code Smell Detection

The following detection rules were implemented:

1. **True Assertions**:
   - Detects unnecessary `self.assertTrue(True)` calls in unit tests.
   - Generates a warning: `Warning('AssertTrueWarning', <line number>, 'useless assert true detected')`.

2. **Assertion-less Tests**:
   - Detects tests that do not contain any assertions.
   - Generates a warning: `Warning('AssertionLessWarning', <line number>, 'it is an assertion less test')`.

3. **Unused Variables**:
   - Detects variables initialized within a test but never used.
   - Generates a warning: `Warning('UnusedVariable', <line number>, 'variable', <variable name>, 'has not been used')`.

4. **Duplicated Setup**:
   - Detects test classes where each test has identical setup code.
   - Generates a warning: `Warning('DuplicatedSetup', <num-dupl-stms>, 'there are <num-dupl-stms> duplicated setup statements')`.

### Code Transformations

The following transformation rules were implemented:

1. **AssertTrue Rewriter**:
   - Replaces `self.assertEquals(x, True)` with `self.assertTrue(x)`.

2. **Variable Inlining**:
   - Eliminates variables used only once and replaces them with their initialization expressions.

3. **Setup Method Extraction**:
   - Extracts duplicate setup code from test methods into a `setUp` method to improve code structure.

## Prerequisites

- Python 3.7+
- `pytest` for running tests: `pip install pytest`
- `ast` module (bundled with Python)
  
## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/your-repo/code-smell-detection.git
   cd code-smell-detection
    ```

2. Install the required dependencies

## How to Run

1. From the root directory, run the following command:

   ```bash
   pytest
   ```

## File Structure

- `rules/:` Contains classes that define the detection rules for code smells.

- `assertion_true.py`: Detects unnecessary assertions.
- `assertion_less.py`: Detects tests without assertions.
- `unused_variable.py`: Detects unused variables.
- `duplicate_setup.py`: Detects duplicated setup code.
- ...
  
- `transformers/:` Contains classes that define the transformation rules for refactoring code.
- `assertion_true_rewriter.py`: Rewrites assertEquals with assertTrue.
- `inline_rewriter.py`: Implements variable inlining.
- `extract_setup_rewriter.py`: Extracts duplicated setup code into a setUp method.
- ...

- `test/:` Contains unit tests for the implemented rules and transformations.
