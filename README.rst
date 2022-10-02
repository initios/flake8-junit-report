flake8-junit-report
===================
Simple tool that converts a flake8 file to junit format.
Use it on your CI server to see the flake8 failures with ease.

.. image:: https://img.shields.io/badge/LICENSE-BSD%203--Clause-brightgreen.svg
.. image:: https://readthedocs.org/projects/flake8-junit-report/badge/?version=latest
    :target: https://readthedocs.org/projects/flake8-junit-report/?badge=latest
    :alt: Documentation Status


.. list-table::

    * - Master
      - .. image:: https://github.com/ricardogarfe/flake8-junit-report/actions/workflows/python-app.yml/badge.svg?branch=master
            :target: https://github.com/ricardogarfe/flake8-junit-report/actions/workflows/python-app.yml
      - .. image:: https://codecov.io/gh/ricardogarfe/flake8-junit-report/branch/master/graph/badge.svg
            :target: https://codecov.io/gh/ricardogarfe/flake8-junit-report
    * - Develop
      - .. image:: https://github.com/ricardogarfe/flake8-junit-report/actions/workflows/python-app.yml/badge.svg?branch=develop
            :target: https://github.com/ricardogarfe/flake8-junit-report/actions/workflows/python-app.yml
      - .. image:: https://codecov.io/gh/ricardogarfe/flake8-junit-report/branch/develop/graph/badge.svg
            :target: https://codecov.io/gh/ricardogarfe/flake8-junit-report

Usage
-----
Create your flake8 file as usual:

.. code:: shell-session

    $ flake8 --output-file flake8.txt

Convert it to JUnit format:

.. code:: shell-session

    $ flake8_junit flake8.txt flake8_junit.xml

Running the tests
-----------------

.. code:: shell-session

    $ pip install -r requirements_dev.txt
    $ tox


Changelog
---------

2016-05-11 **2.1.0**

- Change setuptools `scripts` to `console scripts`.
Now it should works on Windows 

2016-02-13

- Fix bug
- Add version 2.0.1


2016-01-05

- Flake8 file now is always generated, even when there are no errors


2015-07-28

- Add version 2.x.x
- Rolled back python cli to vanilla python
- Renamed binary to flake8_junit


-------------

`CONTRIBUTORS <https://github.com/initios/flake8-junit-report/graphs/contributors>`_
