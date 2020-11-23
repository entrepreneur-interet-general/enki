from apispec.exceptions import APISpecError
from apispec_webframeworks.flask import FlaskPlugin


class FlaskRestfulPlugin(FlaskPlugin):
    """Small plugin override to handle flask-restful resources
    """

    @staticmethod
    def _rule_for_view(view, app=None):
        view_funcs = app.view_functions
        endpoint = None

        for ept, view_func in view_funcs.items():
            if hasattr(view_func, "view_class"):
                view_func = view_func.view_class

            if view_func == view:
                endpoint = ept

        if not endpoint:
            raise APISpecError("Could not find endpoint for view {0}".format(view))

        # WARNING: Assume 1 rule per view function for now
        rule = app.url_map._rules_by_endpoint[endpoint][0]
        return rule
