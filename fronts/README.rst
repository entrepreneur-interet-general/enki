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

