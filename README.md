# GitHub Action - Minimum Dependency Generator

<p align="center">
    <a href="https://github.com/alteryx/minimum-dependency-generator/actions/workflows/unit_tests.yml" target="_blank">
        <img src="https://github.com/alteryx/minimum-dependency-generator/actions/workflows/unit_tests.yml/badge.svg" alt="Unit Tests" />
    </a>
    <a href="https://github.com/alteryx/minimum-dependency-generator/actions/workflows/integration_tests.yml" target="_blank">
        <img src="https://github.com/alteryx/minimum-dependency-generator/actions/workflows/integration_tests.yml/badge.svg" alt="Integration Test" />
    </a>
  <a href="https://codecov.io/gh/alteryx/minimum-dependency-generator">
    <img src="https://codecov.io/gh/alteryx/minimum-dependency-generator/branch/main/graph/badge.svg?token=vRKBsaltyL"/>
  </a>
</p>
<hr>

A GitHub Action to generate minimum Python dependencies.

## Usage

This GitHub Action provides a task to generate the minimum Python given 1 or more requirements. The requirements can be defined in text files or a setup.cfg

#### Text Files
```yaml
steps:
  - name: Run Minimum Dependency Generator
    id: min_dep_gen
    uses: alteryx/minimum-dependency-generator@v3.1
    with:
      paths: 'test-requirements.txt requirements.txt'
      output_filepath: 'generated-min-reqs.txt'
```

#### setup.cfg

```yaml
steps:
  - name: Run Minimum Dependency Generator
    id: min_dep_gen
    uses: alteryx/minimum-dependency-generator@v3.1
    with:
      paths: 'setup.cfg'
      options: 'install_requires setup_requires'
      extras_require: 'dev test'
      output_filepath: 'generated-min-reqs.txt'
```
- The **options** can either be `install_requires`, or `setup_requires`, or both. 
- The **extras_require** is optional, and depends on if you package has plugin-like dependencies. 
- However, either **options** or **extra_requires** must be defined (or both). 
- The **output_filepath** is optional, and specifies the absolute filepath where the minimum requirements should be outputted.


The returned value of a task is available in later steps from the output `min_reqs`.

```
steps.<step id>.outputs.min_reqs
```

## Example

This workflow uses the task to generate minimum dependencies, save the output to a text file, and then will generated an Automated MR if there is a change in the minimum dependencies.

```yaml
# .github/workflows/minimum_dependency_checker.yml
name: Minimum Dependency Checker
on:
  push:
    branches:
      - main
    paths:
      - 'requirements.txt'
      - 'test-requirements.txt'
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout repository
        uses: actions/checkout@v2
        with:
          ref: ${{ github.event.pull_request.head.ref }}
          repository: ${{ github.event.pull_request.head.repo.full_name }}
      - name: Set up python 3.8
        uses: actions/setup-python@v2
        with:
          python-version: 3.8
      - name: Run Minimum Dependency Generator
        id: min_dep_gen
        uses: alteryx/minimum-dependency-generator@v3.1
        with:
          paths: 'test-requirements.txt requirements.txt'
          output_filepath: 'my_package/deps/minimum_requirements.txt'
      - name: Create Pull Request
        uses: FeatureLabs/create-pull-request@v3
        with:
          token: ${{ secrets.REPO_SCOPED_TOKEN }}
          commit-message: Update minimum dependencies
          title: Automated Minimum Dependency Updates
          author: github-actions[bot] <41898282+github-actions[bot]@users.noreply.github.com>
          body: "This is an auto-generated PR with **minimum** dependency updates.
                 Please do not delete the `min-dep-update` branch because it's needed by the auto-dependency bot."
          branch: min-dep-update
          branch-suffix: short-commit-hash
          base: main
```

> If you have a setup.cfg, you will need to change the `paths` argument, and specify either **options** or **extra_requires** (or you can do both).
           
To install this workflow, add the file above to the following location in your repository.

```
.github
└── workflows
    └── minimum_dependency_checker.yml
```
