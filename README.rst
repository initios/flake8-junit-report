flake8-junit-report
===================
Simple tool that converts a flake8 file to junit format.
Use it on your CI server to see the flake8 failures with ease.

.. image:: https://travis-ci.org/initios/flake8-junit-report.svg?branch=develop
    :target: https://travis-ci.org/initios/flake8-junit-report
.. image:: https://coveralls.io/repos/initios/flake8-junit-report/badge.svg
    :target: https://coveralls.io/r/initios/flake8-junit-report
.. image:: https://img.shields.io/badge/LICENSE-BSD%203--Clause-brightgreen.svg

Usage
-----
Create your flake8 file as usual:
.. code-block:: shell-session
    flake8 --output-file flake8.txt

Convert it to JUnit format:
.. code-block:: shell-session
    junitConversor flake8.txt flake8_junit.xml

Running the tests
-----
.. code-block:: shell-session
    pip install -r requirements_dev.txt
    tox
