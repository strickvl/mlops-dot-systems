---
aliases:
- /python/tools/2021/09/14/python-versioning-package-managers
author: Alex Strick van Linschoten
categories:
- python
- tools
date: '2021-09-14'
description: Getting a development environment setup for Python and having to choose
  between pyenv vs virtualenv vs venv
image: images/pyenv_terminal_output.png
layout: post
title: A Baseline Python Development Setup
toc: true

---

The world of Python versioning (and the downstream package versioning) is wild. This [StackOverflow thread](https://stackoverflow.com/questions/41573587/what-is-the-difference-between-venv-pyvenv-pyenv-virtualenv-virtualenvwrappe) gives you a sense of some of the core issues at play. (As an indication of the importance of the issue, even [BDFL](https://www.urbandictionary.com/define.php?term=BDFL) Guido van Rossum himself has the current second most upvoted answer.)

For a really vanilla and close-to-core-python setup, a combination of `venv` and `pip` seem to be the way to go. `venv` is part of the standard library and as such is pretty close to a default option.

For something a bit more involved, that handles dependencies and package installation in a slightly more deft manner, the combination of `pyenv`, `pyenv-virtualwrapper` and `poetry` works really well. I'll detail some of the setup gotchas and usage patterns below.

## `pyenv` for versioning Python itself

`pyenv` lets you install multiple versions of Python on the same machine. The interface to switch between local versions and whatever you've decided will be your `global` option is pretty intuitive.

Visit the [pyenv github page](https://github.com/pyenv/pyenv) for more on installation. (If you're on a Mac you can simply do a `brew install pyenv`.)

To see which versions of Python you have installed locally:

```bash
pyenv versions
```

To see versions of Python which are available for installation:

```bash
pyenv install —list
```

Note that, as I understand it, these versions are not dynamically updated. You get an updated list of new Python versions by updating `pyenv`, in other words.

To install a specific version of Python, and to make it available for use:

```bash
pyenv install 3.9.1
```

To set that version of Python as the global version (i.e. running `python` will use this version by default):

```bash
pyenv global 3.9.1
```

If you are in a project directory and wish to only use a particular version of Python in that directory (and its subdirectories):

```bash
pyenv local 3.8.2
```

This creates a `.python-version` file in that directory with the desired local version.

## `pyenv-virtualenv` for managing virtual environments

`pyenv-virtualenv` is a plugin that connects the work of selecting which version of Python to use (through `pyenv`, which we've previously installed) to the work of creating and running virtual environments to keep code contained in quasi-sandbox environments. When you install packages in virtual environments they don't conflict with other locations where you might have conflicting versions of those same packages installed.

Read installation instructions and the docs [here](https://github.com/pyenv/pyenv-virtualenv). (If you installed `pyenv` with homebrew, be sure to do the same with `pyenv-virtualenv`).

To create a virtual environment for the Python version used with `pyenv`, run `pyenv virtualenv`, specifying the Python version you want and the name of the virtual environment directory:

```bash
pyenv virtualenv 3.8.2 my-virtual-env-3.8.2
```

This will create a virtual environment based on Python 3.8.2 under `$(pyenv root)/versions` in a folder called `my-virtual-env-3.8.2`.

To list what virtual environments have been created and are available to use:

```bash
pyenv virtualenvs
```

As a common workflow pattern, you'd create your directory and `cd` into it, and then you can set the virtual environment you just created as the one to use for that directory:

```bash
mkdir test-project && cd test-project
pyenv local my-virtual-env-3.8.2
```

This should change the prompt in your terminal window and you'll thus know that you're now working out of that virtual environment. Any time you return to that folder you'll automatically switch to that environment.

The manual way of turning on and off virtual environments is:

```bash
pyenv activate env-name
pyenv deactivate env-name
```

To remove a virtual environment from your system:

```bash
pyenv uninstall my-virtual-env
```

(This is the functional equivalent of removing the directories in `$(pyenv root)/versions` and `$(pyenv root)/versions/{version}/envs`.)

## `poetry` for handling package installation and dependencies

[`python-poetry`](https://python-poetry.org) is the latest standard tool for handling package installations and dependency management.

You can use `poetry` without the previous two tools, but really they work best all together. Follow the [installation instructions](https://python-poetry.org/docs/#installation) documented [on their page](https://python-poetry.org/docs/#installation) to get it going.

Then update `poetry`:

```bash
poetry self update
```

`poetry` is one of those tools that's able to update itself.

For basic usage for a new project, you can follow the following workflow. There are two ways to start a new project using `poetry`: using `new` or `init`. For example:

```bash
poetry new some-project-name
```

This will kickstart your new project by creating a bunch of files and a directory structure suitable for most projects, like so:

```
some-project-name
├── pyproject.toml
├── README.rst
├── some-project-name
│   └── __init__.py
└── tests
    ├── __init__.py
    └── test_some-project-name.py
```

You might want to use a `src` folder (above the `some-project-name` in our example) which is fairly commonly used, in which case amend the command as follows:

```bash
poetry new --src some-project-name
```

`poetry init` doesn't do all the extra work of creating a directory and file structure. It merely creates a `pyproject.toml` file interactively, using some smart defaults. For a minimal use of `poetry`, this is definitely the way to go.

The `add` command adds required packages to your `pyproject.toml` and installs them (along with all their dependencies). It does a lot under the hood to make sure that dependencies are correctly resolving before installing. For example:

```bash
poetry add zenml
```

To add packages only to be used in the development environment:

```bash
poetry add --dev zenml
```

To list all installed packages in your current environment / project:

```bash
poetry show
```

To uninstall a package and remove it (and its dependencies) from the project:

```bash
poetry remove zenml
```

To install all relevant packages and dependencies of a project that you've newly cloned into:

```bash
poetry install
```

Note that it is possibly worth creating some custom scripts to handle some of the overhead of using these tools, depending on your common development workflows.
