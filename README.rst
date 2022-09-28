*************
impersonation
*************

.. image:: https://img.shields.io/pypi/v/impersonation
    :target: https://pypi.org/project/impersonation
    :alt: PyPI version
.. image:: https://github.com/rena2damas/impersonation/actions/workflows/ci.yaml/badge.svg
    :target: https://github.com/rena2damas/impersonation/actions/workflows/ci.yaml
    :alt: CI
.. image:: https://codecov.io/gh/rena2damas/impersonation/branch/master/graph/badge.svg
    :target: https://app.codecov.io/gh/rena2damas/impersonation/branch/master
    :alt: codecov
.. image:: https://img.shields.io/badge/code%20style-black-000000.svg
    :target: https://github.com/psf/black
    :alt: code style: black
.. image:: https://img.shields.io/badge/License-MIT-yellow.svg
    :target: https://opensource.org/licenses/MIT
    :alt: license: MIT

A utility that allows a certain routine to run under a given user. To achieve this, a
process will run under the ``uid`` and ``gid`` of the intended user. For that
reason, it is a requirement that the running process has ``SETUID`` and
``SETGID`` capabilities.

Features
========
* decorator for instance methods
* decorator for ``classmethod`` and ``staticmethod``
* decorator for classes

Installation
============
Install the package directly from ``PyPI`` (recommended):

.. code-block:: bash

    $ pip install -U impersonation

Example usage
=============
A simple example on how to work with a ``Flask`` application:

.. code-block:: python

    from impersonation import impersonate

    # it works on functions
    @impersonate("other")
    def printer(string):
        print(string)

    # ... and classes
    @impersonate("other")
    class Printer:
        def __init__(self, prefix=""):
            self.prefix = prefix

        def printer1(self, string):
            print(f"{self.prefix}{string}")

        @staticmethod
        def printer2(string):
            print(string)

Tests & linting 🚥
===============
Run tests with ``tox``:

.. code-block:: bash

    # ensure tox is installed
    $ tox

Run linter only:

.. code-block:: bash

    $ tox -e lint

Optionally, run coverage as well with:

.. code-block:: bash

    $ tox -e coverage

License
=======
MIT licensed. See `LICENSE <LICENSE>`__.
