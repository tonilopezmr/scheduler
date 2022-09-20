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
