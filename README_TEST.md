# Testing your code

Testing your code... a very vast subject. For some it is a fuzzy concept, borderline boring, for others it is the heart of programming; but everyone agrees that testing your code well is not an easy task. In Python, there are libraries to facilitate the writing of tests (`doctest`, `pytest`, `nose`, `hypothesis`, ...), still it remains to make the tests relevant and effective to understand the limits and the flaws of our implementation and design. And then there is the age-old question: have I tested my code enough? It might not be an existential question if you're writing a little library for your friends (though), but if you need to send a satellite into space, or write the guidance program for an intercontinental missile the question is legit.

In this lecture, we will review mostly the concept of unit tests, and put off integration tests.

## Doctest

In this section, we will learn how to use doctest to test functions and modules in Python. A doctest is a way to embed test cases within the documentation of a function or module in Python. The tests are written in the form of interactive Python sessions, and they are used to make sure that the code examples in the documentation are accurate.

Here is an example of a doctest for a simple Python function that calculates the area of a rectangle:

```python
def area(width, height):
    """
    Calculate the area of a rectangle.

    >>> area(5, 10)
    50
    >>> area(2, 3)
    6
    """
    return width * height
```

To run the doctests, you can use the doctest module. For example, you can run the tests for the area function like this:

```python
import doctest

doctest.testmod()
# TestResults(failed=0, attempted=2)
```

This will run all of the doctests in the current module and report any failures.

### Step 1: Write your first doctest

Doctests are well suited for simple function testing. You are going to write your first tests for the fitter functions. Open the `fitter_module.py` module containing the functions. Then, add an `Examples` section to the documentation string (also known as a docstring) to all functions.

### Step 2: Run tests in the terminal

To run the tests, open a terminal, navigate to the directory containing fitter_module.py, and run the following command:

```bash
python -m doctest mymodule.py
```

This won’t display anything unless an example fails, in which case the failing example(s) and the cause(s) of the failure(s) are printed to stdout. Run it with the -v switch instead:

```bash
python -m doctest mymodule.py -v
```

and a detailed report of all examples tried is printed to standard output, along with assorted summaries at the end.

## Pytest

pytest is a testing framework for Python. It is a powerful tool for discovering and running tests, and it has a number of useful features, such as the ability to rerun only the tests that failed during the last run, and support for running tests in parallel.

Here is an example of a simple function that adds two numbers:

```python
def add(a, b):
    return a + b
```

and how you might use pytest to test it

```python
def test_addition():
    assert add(2, 3) == 5
    assert add(-2, 3) == 1
    assert add(2, -3) == -1
    assert add(0, 0) == 0
```

To run this example using pytest, you would save the code above in a file named `test_addition.py`, and then run the pytest command from the command line:

```bash
pytest
```

### Step 1: Use doctest with pytest

You can run any doctest via pytest using the following command:

```bash
pytest --doctest-modules
```

### Step 2: Write the test function

Try to imagine tests for the functions in the `fitter_module.py` module. For example, we wrote a simple test in the file `tests/fitter_test.py`:

```python
from fitter_module import load_data
import pandas as pd

def test_load_data():
    data = load_data('data.csv')
    assert type(data) == pd.DataFrame
```

### Step 3: Parametrize your tests

Instead of writting a dedicated function for each test case, we can refactor the code using the `@pytest.mark.parametrize` decorator and write a single function that will test multiple values. For example we can test the model function as:

```python
from fitter_module import model_function
import pytest

@pytest.mark.parametrize(
    "x,a,b,expected", [(0, 1, 1, 1), (np.pi/2, 1, 1, 2)]
)
def test_model_function(x, a, b, expected):
    assert model_function(x, a, b) == expected
```

### Step 4: Handle exceptions

The `pytest.raises` function allows you to test that a specific exception is raised when certain code is run. This can be useful for verifying that your code is handling errors and exceptions as expected. Here’s an example:

```python
from fitter_module import load_data
import pytest

def test_load_wrong_data():
    # how could we redesign the code to issue a better error?
    with pytest.raises(FileNotFoundError):
        load_data("toto.csv")
```

### Step 5: Coverage

You also check how lines of code are covered by your tests (i.e. are actually executed):

```bash
pytest --doctest-modules --cov=.
```

## Property-based testing

### The limits of the oracle

The vast majority of tests we write are oracle tests, i.e. for a choice of inputs, we compare the output of the test to a value predetermined (by us). These tests are often limited by our imagination (quite limited, especially late at night or under intense stress), and unfortunately by our laziness (who feels like writing 1000 tests for every possible case?). Let's take a very simplistic example, but nevertheless easily generalizable to our more complex developments:

```python
def add_numbers(a: int, b: int) -> int:
    """ add a and b """
    return a + b

def test_add_numbers():
    assert(add_numbers(1, 1) == 2)
```

But have we really verified anything apart from `1 + 1 = 2`? I could have made a bug by writing return `a + a`. And what about the behavior of the `add_numbers` function in general? Just to name the obvious, what happens if we pass `None` as input? A clever mind might say that it would be enough to test on a set of different inputs or add conditions to our function, but that would be underestimating the human mind in the face of laziness and overestimating our imaginative capacities in general in the face of the unexpected.

### From the particular case to the property

The concept of property-based testing was is borrowed from functional programming. To summarize, the idea is no longer to predict the output knowing a particular input, but to determine and test the properties of our function. In the previous example, what particular property(ies) characterizes the `add_numbers` function?

Looking at the function, we see that it is based around the addition operator. Unlike subtraction, addition is commutative, so `add_numbers(a, b) == add_numbers(b, a)`. But we could have made a bug by writing the operator `*` instead of `+` and the test would still be valid... So what other property distinguishes addition from multiplication? The neutral element! `add_numbers(a, 0) == a` is not satisfied for multiplication.

We have therefore isolated at least 2 properties which allow us to test our function (its implementation) without having to resort to explicit input/output values (well almost, see later).
Finding properties is the real difficulty of this type of test. Here are some properties that often come up in our scientific developments (the list is endless!):

- The invariants
- Inverses (invertible function)
- Idempotence
- Properties of internal composition laws: associativity, commutativity...
- Structural induction (Solve a smaller problem first)
- Hard to prove, easy to verify

### Hypothesis: the basis

Let's move on to the Python implementation of these property-based tests. The [Hypothesis](https://hypothesis.readthedocs.io/en/latest/) library provides support for writing and running such tests. To install Hypothesis, nothing could be easier: `pip install hypothesis`. See for example one test in `tests/fitter_test.py`:

```python
from hypothesis import given, strategies
import numpy as np

@given(
    a=strategies.floats(
        allow_nan=False,
        allow_infinity=False,
        min_value=-1000,
        max_value=1000
    ),
    b=strategies.floats(
        allow_nan=False,
        allow_infinity=False,
        min_value=-1000,
        max_value=1000
    ),
)
def test_idempotence(a, b):
    # what if we release the bounds?
    x0 = np.arange(0., 4 * np.pi, 0.1)
    y0 = a * np.sin(x0) + b

    params0, errs0 = fit_data(x0, y0)

    y1 = params0[0] * np.sin(x0) + params0[1]
    params1, errs1 = fit_data(x0, y1)

    assert np.allclose(params0[0], params1[0], atol=1e-6)
```

Let's take the time to observe the syntax. First there is our `fit_data` function, and a `test_idempotence` test. The test is decorated so we are composing functions. The test has two inputs (and the nice programmer even specified the type), and the decorator specifies the strategy for generating the test dataset: we want to test our function on floats (double precision in Python by default!) between -1000 and 1000. Generally speaking, you can generate just about any type for the test set.

This test reflect the fact that our fitting function should be indempotent: if I first fit for the model parameters, and then input data generated from these parameters into our fitting function, I should get the same set of model parameters fitted.

If you run this piece of code (pytest integrates with hypothesis):

```bash
pytest --doctest-modules --cov=.
```

nothing should happen: a good sign is that the tests passed. Modify the test to fail (e.g. release all the conditions in the decorator), and observe the response from hypothesis. The library returns an example of entries for which the test does not pass. By default, the library only returns a single example, and it performs a shrinking pass, i.e. for numeric values, as intuitive as possible (whatever it means...). See more information [here](https://hypothesis.readthedocs.io/en/latest/settings.html#controlling-what-runs).

Note the failures of this test are a sign of a bad implementation design (boundary conditions, input `NaN`, etc.).

### Health checks

Not only does Hypothesis expose tools for performing tests, but it also offers features for detecting bad programming practices that can interfere with the proper maintenance and execution of code:

- Tests that require data that is too complex and that slow down execution.
- Tests that do not explore the parameter space enough.
- Bad recursion strategies (understand: which diverges too much)
- Tests that have no chance of completing before the end of the world.

See [here](https://hypothesis.readthedocs.io/en/latest/healthchecks.html) for more information.

### Exercise

You probably have a lot of code with you, why not try implementing property-based testing in your existing test suites?

### A bit of demystification

In property-based tests, unlike example-based tests (oracle), we do not specify any particular values: only the type of the input data and the property to be tested. Hypothesis will take care of actually executing the test. Magic you would say to me.

Almost magical. There is still a lot of smoke in most cases. If we take our `add_number` function, we suspect that we cannot test the whole set of floats... Under the hood, there is therefore a random number generator, which stops at some point given (configurable, but not infinite). So basically I could have generated a set of random integers, written my traditional oracle test, and put a good old for loop in front of it:

```python
import sys
import numpy as np

n_iteration = 1000
data_in = np.random.randint(-sys.maxsize - 1, sys.maxsize, (n_iteration, 2))
for a, b in data_in:
    assert(add_numbers(a, b) == add_numbers(b, a))
```

Of course, this is possible for simple cases, and there are fortunately a large number of cases where property-based tests do not really have simple equivalents.

## Finally, what should I choose for my tests?

Oracle tests or property tests? My answer is: both! If you're looking for some motivations for using property-based testing, here are a few that are quite relevant:

- Property-based tests are generally more generic than Oracle tests.
- They expose a more concise description of the requirements and expected behavior of our code than oracles tests.
- As a result, a property-based test can replace a large number of oracle tests.
- By delegating input generation to specialized tools, property-based testing will be more efficient in finding implementation problems, particular untreated values...
- Property-based tests require more thinking effort than oracle tests, and therefore they allow for better introspection.
- As a result, code design is often better.

But it's not always easy or relevant to find properties, so we can still rely on oracle tests. It is the combination of both that will make your code even more robust :-) To go further, I invite you to read this quite interesting [blog post](https://fsharpforfunandprofit.com/series/property-based-testing/) (based on F# - but the idea is the same).

To finish, and to meditate: programming is not just a matter of lines of code, it is above all conceiving a design that makes it possible to fulfill objectives.
