[![Tests](https://github.com/martineberlein/evogfuzzplusplus/actions/workflows/test_evogfuzz.yml/badge.svg)](https://github.com/martineberlein/evogfuzzplusplus/actions/workflows/test_evogfuzz.yml)
&nbsp;

# EvoGFuzz

Welcome to the **EvoGFuzz** repository! This repository houses the source code for the innovative grammar-based fuzzing tool EvoGFuzz, as first documented in our paper _Evolutionary Grammar-Based Fuzzing_ that was presented at [SSBSE'2020](http://ssbse2020.di.uniba.it/).

## Quickstart

To provide an immediate understanding of EvoGFuzz's capabilities, let's dive into a simple yet illustrative example using a program we've labeled **The Calculator**.

The Calculator program is written in Python and is capable of evaluating mathematical expressions, including arithmetic equations and trigonometric functions:

```python
import math

def arith_eval(inp) -> float:
    return eval(
        str(inp), {"sqrt": math.sqrt, "sin": math.sin, "cos": math.cos, "tan": math.tan}
    )
```

We use an oracle function to discern between normal and faulty behavior:

```python 
from evogfuzz.oracle import OracleResult

def oracle(inp: str) -> OracleResult:
    try:
        arith_eval(inp)
        return OracleResult.NO_BUG
    except ValueError:
        return OracleResult.BUG
    
    return OracleResult.NO_BUG
``` 

We can see this in action by testing a few initial inputs:

```python
initial_inputs = ['cos(10)', 'sqrt(28367)', 'tan(-12)', 'sqrt(3)']
print([(x, oracle(x)) for x in initial_inputs])
```

This will yield the following output:

```
[('cos(10)', OracleResult.NO_BUG),
 ('sqrt(28367)', OracleResult.NO_BUG),
 ('tan(-12)', OracleResult.NO_BUG),
 ('sqrt(3)', OracleResult.NO_BUG)]
```

We apply our `EvoGFuzz` class to carry out fuzz testing using evolutionary grammar-based fuzzing. This is aimed at uncovering potential defects in our 'calculator' function.

First, we must define the input format of the calculator using a grammar:

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

With the grammar in place, we can initialize **EvoGFuzz** with this grammar, the sample inputs, and the oracle function:

```python
from evogfuzz.evogfuzz_class import EvoGFuzz

epp = EvoGFuzz(
    grammar=grammar,
    oracle=oracle,
    inputs=initial_inputs,
    iterations=10
)
```

Upon creating the `EvoGFuzz` instance, we can execute the fuzzing process. The `fuzz()` method runs the fuzzing iterations, evolving the inputs based on our fitness function, and returns a collection of inputs that lead to exceptions in the 'calculator' function.

```python
found_exception_inputs = epp.fuzz()
```

Lastly, we can examine the inputs that resulted in exceptions.
This output can provide valuable insight into potential weaknesses in the 'calculator' function that need to be addressed.

```python
for inp in list(found_exception_inputs)[:20]:
    print(str(inp).ljust(30), inp.oracle)
```

Output:

````
sqrt(-61)                      BUG
sqrt(-373)                     BUG
sqrt(-78)                      BUG
sqrt(-4)                       BUG
sqrt(-6)                       BUG
sqrt(-73)                      BUG
sqrt(-45)                      BUG
sqrt(-87738)                   BUG
sqrt(-5587)                    BUG
sqrt(-823853)                  BUG
sqrt(-38317)                   BUG
sqrt(-83)                      BUG
sqrt(-7)                       BUG
sqrt(-43)                      BUG
sqrt(-71337)                   BUG
sqrt(-3737437)                 BUG
sqrt(-17)                      BUG
sqrt(-33)                      BUG
sqrt(-57662773794)             BUG
sqrt(-731)                     BUG
````

This process illustrates the power of evolutionary grammar-based fuzzing in identifying new defects within our system.
By applying evolutionary algorithms to our fuzzing strategy, we can guide the search towards more defect-prone regions of the input space.

## Install, Development, Testing, Build

### Install
If all external dependencies are available, a simple pip install evogfuzz suffices.
We recommend installing EvoGFuzz inside a virtual environment (virtualenv), commands differ slightly for MacOS/Linux and Windows users:

<table>
<tr>
<th style="font-weight: normal;">MacOS/Linux</th>
<th style="font-weight: normal;">Windows</th>
</tr>
<tr>
<td>

```
python3.10 -m venv venv
source venv/bin/activate

pip install --upgrade pip
pip install evogfuzz
```
</td>
<td>

```
#create a venv with the specified version
py -3.10 -m venv venv3_10

Set-ExecutionPolicy -ExecutionPolicy RemoteSigned
venv3_10/Scripts/Activate.ps1

python -m pip install --upgrade pip
pip install evogfuzz
```
</td>
</tr>
</table>

Now, the evogfuzz command should be available on the command line within the virtual environment.

### Development and Testing

For development, we recommend using EvoGFuzz inside a virtual environment (virtualenv).
By thing the following steps in a standard shell (bash), one can run the EvoGFuzz tests:

<table>
<tr>
<th style="font-weight: normal;">MacOS/Linux</th>
<th style="font-weight: normal;">Windows</th>
</tr>
<tr>
<td>

```
git clone https://github.com/martineberlein/evogfuzzplusplus.git
cd evogfuzzplusplus/

python3.10 -m venv venv
source venv/bin/activate

pip install --upgrade pip

# Run tests
pip install -e .[dev]
python3 -m pytest
```
</td>
<td>

```
git clone https://github.com/martineberlein/evogfuzzplusplus.git
cd evogfuzzplusplus/

py -3.10 -m venv venv3_10
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned
venv3_10/Scripts/Activate.ps1

python -m pip install --upgrade pip

# Run tests
pip install -e .[dev]
python -m pytest
```
</td>
</tr>
</table>


### Build

EvoGFuzz is build locally as follows:

<table>
<tr>
<th style="font-weight: normal;">MacOS/Linux</th>
<th style="font-weight: normal;">Windows</th>
</tr>
<tr>
<td>

```
git clone https://github.com/martineberlein/evogfuzzplusplus.git
cd evogfuzz/

python3.10 -m venv venv
source venv/bin/activate

pip install --upgrade pip
pip install --upgrade build
python3 -m build
```
</td>
<td>

```
git clone https://github.com/martineberlein/evogfuzzplusplus.git
cd evogfuzz/

py -3.10 -m venv venv3_10
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned
venv3_10/Scripts/Activate.ps1

python -m pip install --upgrade pip
pip install --upgrade build
python -m build
```
</td>
</tr>
</table>


Then, you will find the built wheel (*.whl) in the dist/ directory.
