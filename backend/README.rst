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

.. code-block:: bash

   $ make up

For Local Testing
^^^^^^^^^^^^^^^^^

Make sure you have the latest pip version!

.. code-block:: bash

   $ pip install --upgrade pip

Install the requirements

.. code-block:: bash

   $ pip install -r requirements.txt
   $ pip install -r requirements.dev.txt


# Run tests
.. code-block:: bash

   $ pytest src/tests