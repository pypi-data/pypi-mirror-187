# Contributing

## Code
1. To be able to import the package under development in the Python REPL, run the following:

   ```shell
   pip install -U pip setuptools -e .
   ```

2. Install [pre-commit](https://pre-commit.com/)

   ```shell
   pip install pre-commit
   pre-commit install
   ```
> this will be checked with a github action,
> if you don't format it, the checks will fail

3. Document your code, write tests if needed, use feature branches to contribute.

   To run tests use [tox](https://tox.wiki):
   Literally just:
   ```shell
   tox
   ```
   And to run the linter:
   ```shell
   tox -e lint
   ```

## Documentation Improvements

`nptr-cli` uses sphinx for documentation, the documentation is written inside of the docstrings.
It is also configured to use [CommonMark](https://commonmark.org/)
with the [MyST](https://myst-parser.readthedocs.io/en/latest/index.html) extension.

When working on documentation changes in your local machine, you can
compile them using [tox](https://tox.wiki):

```shell
tox -e docs
```

the output files are in docs/_build/html
