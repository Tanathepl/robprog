# Automation of workflows

Documentation, tests, code linting... If you had to manually run them after each code addition or deletion, you would give up quickly! Instead, we advice to use the concept of `Continuous Integration`. In short, there are tools that will run this for you automatically each time you modify the code, and give you a summary report so that you only have to focus on changes.

There are many options to set up a continuous integration. In this lecture, we will use the tools integrated with the GitHub platform, but there are many other ways!

## Set up the CI in GitHub

Simply create a folder `.github/workflows` at the root of your repository. You are good to go!

## Documentation

Maintaining documentation is more efficient if the execution chain is automated. The easiest way to do this is to use continuous integration to re-generate documentation automatically as code changes. You will cover the notions of continuous integration later, but here is a minimal example on the GitHub CI to build the doc and publish it on github pages automatically each time you perform a `push` action in the repository:

```yaml
name: GitHub Pages

on:
  push:
    branches:
      - main
  pull_request:

jobs:
  deploy:
    runs-on: ubuntu-22.04
    permissions:
      contents: write
    steps:
      - uses: actions/checkout@v3

      - name: Setup Python
        uses: actions/setup-python@v3
        with:
          python-version: '3.9'

      - name: Install dependencies
        run: pip install -r requirements.txt

      - name: Deploy
        run: |
          cd doc
          make html
          mv build/html ../public

      - name: Deploy
        uses: peaceiris/actions-gh-pages@v3
        if: ${{ github.ref == 'refs/heads/main' }}
        with:
          github_token: ${{ secrets.GITHUB_TOKEN }}
          publish_dir: ./public
```

Then once the Actions is successful, go to the GitHub website, and select `Settings` on your repository. Click on `Pages`, and configure the `gh-pages` as the deployment branch, and the folder `root`. Save and enjoy the site live!

## Static program analysis

```yaml
name: PEP8

on:
  push:
    branches:
      - main
  pull_request:

jobs:
  build:

    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: [3.11]

    steps:
    - uses: actions/checkout@v2
    - name: Set up Python ${{ matrix.python-version }}
      uses: actions/setup-python@v2
      with:
        python-version: ${{ matrix.python-version }}
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install flake8
    - name: Main
      run: |
        flake8 example/*.py --count --show-source --statistics --ignore=W605
    - name: Tests
      run: |
        flake8 tests/*.py --count --show-source --statistics
```

## Tests

```yaml
name: Tests

on:
  push:
    branches:
      - main
  pull_request:

jobs:
  build:

    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: [3.11]

    steps:
    - uses: actions/checkout@v2
    - name: Set up Python ${{ matrix.python-version }}
      uses: actions/setup-python@v2
      with:
        python-version: ${{ matrix.python-version }}

    - name: Install dependencies
      run: pip install -r requirements.txt

    - name: Run tests
      run: |
        pytest --doctest-modules --cov=.
```
