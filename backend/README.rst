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
   $ pip install -r requirements.dev.txt

.. code-block:: bash

   $ pip install -e ./src

Start the app ressources (pg):

.. code-block:: bash

   $ make ressources

Copy the .env.sample file in `backend/.env.sample` and rename the new file to `backend/.env`

Launch the app :

.. code-block:: bash

   $ flask run

# Runnig entire app with docker (no need for `make ressources` in this case):


To run the application in docker environement (it will also build the app image)

.. code-block:: bash

   $ make up
