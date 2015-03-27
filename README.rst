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
      - .. image:: https://travis-ci.org/initios/flake8-junit-report.svg?branch=master
            :target: https://travis-ci.org/initios/flake8-junit-report
      - .. image:: https://coveralls.io/repos/initios/flake8-junit-report/badge.svg?branch=master
            :target: https://coveralls.io/r/initios/flake8-junit-report?branch=master
    * - Develop
      - .. image:: https://travis-ci.org/initios/flake8-junit-report.svg?branch=develop
            :target: https://travis-ci.org/initios/flake8-junit-report
      - .. image:: https://coveralls.io/repos/initios/flake8-junit-report/badge.svg?branch=develop
            :target: https://coveralls.io/r/initios/flake8-junit-report?branch=develop

Usage
-----
Create your flake8 file as usual:

.. code:: shell-session

    $ flake8 --output-file flake8.txt

Convert it to JUnit format:

.. code:: shell-session

    $ junit_conversor flake8.txt flake8_junit.xml

Running the tests
-----------------

.. code:: shell-session

    $ pip install -r requirements_dev.txt
    $ nosetests

Contributions
-------------
.. _Authors: AUTHORS.rst

 Check `authors file`_.

 .. _authors file: AUTHORS.rst 
