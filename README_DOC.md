# Documentation

**Challenge:** The great post-doc of the group has left. He was working on a great code to estimate the parameters of a model from the data of a top secret experiment. He left the code, but he never wrote the documentation... It is your turn now to document it before the next release!

You can (fork and) clone the repository on your computer using git:

```bash
git clone ...
```

----

## Step 0: Software Design Documentation

* Why the code has been created? What were the motivations, the challenges?
* Brief description of the concept
* Technical implementation, external dependencies
* Other existing methods?

----

## Step 1: Identifying the users

* What is it: a framework, a library, an executable script?
* Is the code open source? On a collaborative platform?
* Are there several contributors? Already identified users?

---

## Setp 2: Documenting the code

* Using docstrings, document the code.
  See <a href="https://www.python.org/dev/peps/pep-0257">PEP 257</a>,
  <a href="https://www.python.org/dev/peps/pep-0258">PEP 258</a>,
  <a href="https://numpydoc.readthedocs.io/en/latest/format.html">numpydoc</a>,
  <a href="https://google.github.io/styleguide/pyguide.html#38-comments-and-docstrings">google</a>
* Add <a href="https://docs.python.org/3/library/typing.html">type hints</a>
* You want to refactor the code? That's normal :-)
---

## Step 3: High level documentation

Let's make a user manual using [sphinx](https://www.sphinx-doc.org/en/master/). First make sure you are working with the correct environment:

```bash
conda env create -f environment.yml
conda activate robprog
```

Then, at the root of the repository, make a new folder called `doc`, and execute:

```bash
cd doc
sphinx-quickstart
```

Follow the instructions on screen (editable later), and finally build the documentation:

```bash
make html
```

You can then open the file `doc/build/html/index.html` in a browser and see your documentation! It is empty for the moment, but you can edit it to add more pages such as installation, quickstart, tutorial, or even include the code docstrings...

---

## Step 4: Automation

Maintaining documentation is more efficient if the execution chain is automated. The easiest way to do this is to use continuous integration to re-generate documentation automatically as code changes. You will cover the notions of continuous integration later, but here is a minimal example on the GitHub/GitLab CI to build the doc and publish it on github/gitlab pages automatically:

### GitHub example

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

### GitLab example

```yaml
image: python:3.9-alpine

pages:
  script:
  - pip install -r requirements.txt
  - cd doc
  - make html
  - mv build/html ../public
  artifacts:
      paths:
      - public
  only:
  - master
```


---
