# Scheduler

# Quickstart

	$ poetry install	
	$ scheduler -h
	$ scheduler 16:10 < input.txt

Or (given this program takes stdin):

	$ cat input.txt | scheduler 16:10

# Running Static Tests

It includes linter and type check to ensure the code consistency among the different modules.

$ poetry shell
$ nox -s fmt_check
$ nox -s lint
$ nox -s type_check

# Running Tests

Installs pytest and runs the suit in a py8, py8, py10 environment.

	$ poetry shell
	$ nox -s test

You can run static tests and unit / integration tests using nox command.

	$ nox

# Packaging

Creates a pip installable zip file and wheel file using poetry.

	$ poetry build


# Why?

## Why Did I do it with Python?

- As this is a simple script to be ran using the CLI, I used Python with Poetry to easily use, install, this example using CLI

## Why Did I include Poetry?

- Poetry is a python packaging and dependency manager to install the dependencies, run tests and also to package the app as if it's an SDK or library.
