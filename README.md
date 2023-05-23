[![Tests](https://github.com/martineberlein/evogfuzzplusplus/actions/workflows/test_evogfuzz.yml/badge.svg)](https://github.com/martineberlein/evogfuzzplusplus/actions/workflows/test_evogfuzz.yml)
&nbsp;

EvoGFuzz
=======

This repo contains the code to execute, develop and test our grammar-based fuzzing tool **EvoGFuzz**,
which was first described in our paper _Evolutionary Grammar-Based Fuzzing_ accepted at [SSBSE'2020](http://ssbse2020.di.uniba.it/).

**Example**

To illustrate EvoGFuzz’s capabilities, we start with a quick motivating example.
First, let us introduce our program under test: **The Calculator**. 

```python
import math

def arith_eval(inp) -> float:
    return eval(
        str(inp), {"sqrt": math.sqrt, "sin": math.sin, "cos": math.cos, "tan": math.tan}
    )
```

This infamous program accepts arithmetic equations, trigonometric functions and allows us to calculate the square root.
To help us determine faulty behavior, i.e., a crash, we implement an evaluation function

```python 
def prop(inp: str) -> bool:
    try:
        arith_eval(inp)
        return False
    except ValueError:
        return True
    return False
``` 

that takes an input file and returns whether a bug occurred during the evaluation of the mathematical equations (`BUG=True`, `NO_BUG=False`). 
We can now test the calculator with some sample inputs:

```python
inputs = ['cos(10)', 'sqrt(28367)', 'tan(-12)', 'sqrt(-3)']
print([(x, prop(x)) for x in inputs])
```

The output looks like this:

```
[('cos(10)', False),
 ('sqrt(28367)', False),
 ('tan(-12)', False),
 ('sqrt(-3)', True)]
```

We see that `sqrt(-3)` results in the failure of our calculator program.
We can now use **EvoGFuzz** to learn a _probabilistic grammar_ that describes all failing inputs. 

First, we need to define the input format of the calculator with a grammar:
```python
import string

grammar = {
    "<start>": ["<arith_expr>"],
    "<arith_expr>": ["<function>(<number>)"],
    "<function>": ["sqrt", "sin", "cos", "tan"],
    "<number>": ["<maybe_minus><onenine><maybe_digits>"],
    "<maybe_minus>": ["", "-"],
    "<onenine>": [str(num) for num in range(1, 10)],
    "<digit>": list(string.digits),
    "<maybe_digits>": ["", "<digits>"],
    "<digits>": ["<digit>", "<digit><digits>"],
}
```

Then, we can call **EvoGFuzz** with the grammar, some sample inputs, and the evaluation function (program under test).

```python
from evogfuzz.evogfuzz_class import EvoGFuzz
from evogfuzz.fitness_functions import fitness_function_failure as fitness_function

epp = EvoGFuzz(
    grammar=grammar,
    oracle=prop,
    inputs=inputs,
)

epp.execute()
```

By default, **EvoGFuzz** will do _10_ iterations of its evolutionary optimization.
Finally, **EvoGFuzz** returns the probabilistic grammar that describes the failure-inducing inputs.

For our calculator, the learned grammar looks something like this:

```python
{'<start>': [('<arith_expr>', {'prob': None})],
 '<arith_expr>': [('<function>(<number>)', {'prob': None})],
 '<function>': [('sqrt', {'prob': 1.0}),
                ('sin', {'prob': 0.0}),
                ('cos', {'prob': 0.0}),
                ('tan', {'prob': 0.0})],
 '<maybe_minus>': [('', {'prob': 0.0}), ('-', {'prob': 1.0})],
 '<number>': [('<maybe_minus><onenine><maybe_digits>', {'prob': None})],
 '<digit>': [...],
 '<digits>': [('<digit>', {'prob': 0.5}), ('<digit><digits>', {'prob': 0.5})],
 '<maybe_digits>': [('', {'prob': 0.0}), ('<digits>', {'prob': 1.0})],
 '<onenine>': [('1', {'prob': 0.26448026237029304}),
               ('2', {'prob': 0.13854210013644921}),
               ('3', {'prob': 0.07928598549297672}),
               ('4', {'prob': 0.0038772429661826603}),
               ('5', {'prob': 0.21379401641055015}),
               ('6', {'prob': 0.009018562666488764}),
               ('7', {'prob': 0.09581593224585401}),
               ('8', {'prob': 0.008346286752892956}),
               ('9', {'prob': 0.18683961095831245})]}
```

By looking at the probabilities of the competing alternatives of the production rules, we quickly spot that all failure-inducing inputs use the `sqrt(x)` function and contain a `<maybe_minus> == '-'`.

By following the learned probabilities, we can now use this probabilistic grammar to produce new inputs failure-inducing inputs  

```python
from fuzzingbook.ProbabilisticGrammarFuzzer import ProbabilisticGrammarFuzzer

# Use probabilistic fuzzer with final grammar
fuzzer = ProbabilisticGrammarFuzzer(epp._probabilistic_grammars[-1][0])

for _ in range(10):
    inp = fuzzer.fuzz()
    print(inp, prop(inp))
```

Output:

```python
('sqrt(-38584459)', True)
('sqrt(-750764974567536585)', True)
('sqrt(-79460500)', True)
('sqrt(-364)', True)
('sqrt(-75)', True)
('sqrt(-35554653089074)', True)
('sqrt(-77549465054)', True)
('sqrt(-256)', True)
('sqrt(-28550)', True)
('sqrt(-374574)', True)
```

We see that all generated inputs now trigger the failure of the calculator.

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
