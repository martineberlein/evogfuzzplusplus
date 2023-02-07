[![Tests](https://github.com/martineberlein/evogfuzzplusplus/actions/workflows/test_evogfuzz.yml/badge.svg)](https://github.com/martineberlein/evogfuzzplusplus/actions/workflows/test_evogfuzz.yml)
&nbsp;

EvoGFuzz
=======

This repo contains the code to execute, develop and test our grammar-based fuzzing tool **EvoGFuzz**.

## Install, Development, Testing, Build

### Install
If all external dependencies are available, a simple pip install evogfuzz suffices.
We recommend installing EvoGFuzz inside a virtual environment (virtualenv):

```
python3.10 -m venv venv
source venv/bin/activate

pip install --upgrade pip
pip install evogfuzz
```

Now, the evogfuzz command should be available on the command line within the virtual environment.

### Development and Testing

For development, we recommend using EvoGFuzz inside a virtual environment (virtualenv).
By thing the following steps in a standard shell (bash), one can run the EvoGFuzz tests:

```
git clone https://github.com/martineberlein/evogfuzz.git
cd evogfuzz/

python3.10 -m venv venv
source venv/bin/activate

pip install --upgrade pip

# Run tests
pip install -e .[dev]
python3 -m pytest
```

### Build

EvoGFuzz is build locally as follows:

```
git clone https://github.com/martineberlein/evogfuzz.git
cd evogfuzz/

python3.10 -m venv venv
source venv/bin/activate

pip install --upgrade pip
pip install --upgrade build
python3 -m build
```

Then, you will find the built wheel (*.whl) in the dist/ directory.

# How to setup EvoGFuzz?

_EvoGFuzz++_ requires the tool `tribble`. It needs to be installed independently.

```
Setup Script will follow soon
```

# How to run EvoGFuzz?


```
python3 evogfuzz.py --output <out_dir> --target <subject_driver>
```

where
* `<output_dir>` is where evogfuzz's output shows up
* `<subject_driver>` is a python file which contains a ``execute_samples()`` method,
  which returns the driver object for the program under test.

The ``subject_driver`` for existing subjects can be found in the folders of the subjects/ folder.
If you e.g. want to run Rhino you would invoke

```
python3 evogfuzz.py --output ../results --target ../subjects/Rhino/subject_driver.py
```

# How to add subjects?

* `<grammar_driver>` ..
* `<subject_driver>` ..

# Requirements

In order to run EvoGFuzz, the ANTLR parser generator (Version 4.7.1) is required.
Additionally, the class path for antlr4 needs to be exported.

```
export CLASSPATH=".:/<path-to-ANTLR-library>/antlr-4.5-complete.jar:$CLASSPATH"
java org.antlr.v4.Tool
```
