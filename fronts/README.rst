# Fronts

This project uses [Nx](https://nx.dev) to handle the frontends, it tries to make most of the code reusable.

The structure should be like this :

apps
  -> op18-couv-ops (react app using : core-couv-ops, ui-components)
  -> enki-reports (angular app using : core-reports, ui-components)
lib
  -> core-couv-ops (core logic for couv-ops, using typescript and redux)
  -> core-reports (core logic for reports, using typescript and redux)
  -> ...
  -> utils (utilities in typecript reusable on all projects)
  -> ui-components (could be Web Component lib, so that it is usable both by angular and react)

# Setup

Installation
------------

Pre-requisite
^^^^^^^^^^^^^

- node 12.18

For developement :

Go in `fronts` folder

Install dependencies:

.. code-block:: bash

   $ npm install

In front/apps/couv-ops: copy the file `.env.sample` and rename it to `.env`
`.env` should not be versionned in git, it is used for hosting env variables.

You can choose from those variables to have the backend simulated in memory or to actually call the backend (if it is running).

Once the variable is set you can start the front with :

.. code-block:: bash

   $ npm start couv-ops

To launch the test of core-couv-ops:

.. code-block:: bash

   $ npm test core-couv-ops



