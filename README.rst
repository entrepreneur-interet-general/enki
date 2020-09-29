==========
Repository
==========

- 1 Backend (shared)
- 3 Front
    * front commandment (dedicated to the firefighter on a daily basis: operational coverage management, simulator, decision support,...)
    * front passive watch (intended for mayors, elected officials, general): high-level watch, alerts)
    * front crisis orchestration : tasks management


===============
Sapeurs Backend
===============

We followed the guidelines of [cosmic python book](https://www.cosmicpython.com/book/preface.html)
to structure our repository.

|test-status|

Installation
------------

Pre-requisite
^^^^^^^^^^^^^

- python 3.8

For development
^^^^^^^^^^^^^^^

Before you start, create a virtual environment and activate it.

.. code-block:: bash

   $ python3 -m venv venv
   $ source venv/bin/activate

Make sure you have the latest pip version!

.. code-block:: bash

   $ pip install --upgrade pip

Install the requirements

.. code-block:: bash

   $ pip install -r requirements.txt

Export environment variables :
.. code-block:: bash
   $ export FLASK_ENV=development
   $ export FLASK_APP=src/entrypoints/flask_app

Launch the app :

.. code-block:: bash

   $ flask run

For production
^^^^^^^^^^^^^^^

Docker is comin'