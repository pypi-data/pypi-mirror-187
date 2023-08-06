========
Overview
========

.. start-badges

.. list-table::
    :stub-columns: 1

    * - docs
      - |docs|
    * - tests
      - | |github-actions|
        | |coveralls| |codecov|
    * - package
      - | |version| |wheel| |supported-versions| |supported-implementations|
        | |commits-since|
.. |docs| image:: https://readthedocs.org/projects/beancount-mbank/badge/?style=flat
    :target: https://beancount-mbank.readthedocs.io/
    :alt: Documentation Status

.. |github-actions| image:: https://github.com/lstrzepek/beancount-mbank/actions/workflows/github-actions.yml/badge.svg
    :alt: GitHub Actions Build Status
    :target: https://github.com/lstrzepek/beancount-mbank/actions

.. |coveralls| image:: https://coveralls.io/repos/lstrzepek/beancount-mbank/badge.svg?branch=main&service=github
    :alt: Coverage Status
    :target: https://coveralls.io/r/lstrzepek/beancount-mbank

.. |codecov| image:: https://codecov.io/gh/lstrzepek/beancount-mbank/branch/main/graphs/badge.svg?branch=main
    :alt: Coverage Status
    :target: https://codecov.io/github/lstrzepek/beancount-mbank

.. |version| image:: https://img.shields.io/pypi/v/beancount-mbank.svg
    :alt: PyPI Package latest release
    :target: https://pypi.org/project/beancount-mbank

.. |wheel| image:: https://img.shields.io/pypi/wheel/beancount-mbank.svg
    :alt: PyPI Wheel
    :target: https://pypi.org/project/beancount-mbank

.. |supported-versions| image:: https://img.shields.io/pypi/pyversions/beancount-mbank.svg
    :alt: Supported versions
    :target: https://pypi.org/project/beancount-mbank

.. |supported-implementations| image:: https://img.shields.io/pypi/implementation/beancount-mbank.svg
    :alt: Supported implementations
    :target: https://pypi.org/project/beancount-mbank

.. |commits-since| image:: https://img.shields.io/github/commits-since/lstrzepek/beancount-mbank/v0.1.0.svg
    :alt: Commits since latest release
    :target: https://github.com/lstrzepek/beancount-mbank/compare/v0.1.0...main



.. end-badges

Beancount Importer for mBank (PL) CSV exports


Installation
============

::

    pip install beancount-mbank

You can also install the in-development version with::

    pip install https://github.com/lstrzepek/beancount-mbank/archive/main.zip


Documentation
=============


https://beancount-mbank.readthedocs.io/


Development
===========

To run all the tests run::

    tox

Note, to combine the coverage data from all the tox environments run:

.. list-table::
    :widths: 10 90
    :stub-columns: 1

    - - Windows
      - ::

            set PYTEST_ADDOPTS=--cov-append
            tox

    - - Other
      - ::

            PYTEST_ADDOPTS=--cov-append tox
