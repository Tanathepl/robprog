# Static program analysis

Static program analysis is the analysis of computer programs performed without executing them. This is typically used to make sure syntax is uniform across different peices of code, and it will check pre-defined rules to be satisfied. In Python, this will be used to check that Python coding style is respected ([PEP8](https://peps.python.org/pep-0008/)), or to perform [type checks](https://docs.python.org/3/library/typing.html).

You can read all rules, or simply use tools that will do it for you such as `flake8` for the linting, or `mypy` for the type checks. Try for example:

```bash
flake8 fitter.py --count --show-source --statistics
```

or

```bash
mypy example/fitter_module_doc.py --ignore-missing-imports
```

In my opinion, it also reduces the number of mistakes and force to think about the design. In most languages, automatic formatting (e.g. `black` in Python, `clang-format` in C++) also seems like the way to go. Mandating that everyone always is probably a good idea. It is good not to have too much democracy and freedom in team decision-making on these issues; uniformity matters much more than any particular style choice.