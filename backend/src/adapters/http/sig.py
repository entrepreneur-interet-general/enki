import requests
from requests import Response
from typing import Union, List
import os

SIG_API_URL = os.environ.get("SIG_API_URL")
SIG_API_KEY = os.environ.get("SIG_API_KEY")


class SigApiAdapter:
    @staticmethod
    def code_territory_search(postal_code: Union[str, List[str]], insee_code: Union[str, List[str]]) -> Response:
        url = f"{SIG_API_URL}/decoupage-administratif/territoire/codes"

        querystring = {"codesInsee": insee_code, "codesPostaux": postal_code}

        headers = {
            'x-api-key': SIG_API_KEY
        }

        response = requests.request("GET", url, headers=headers, params=querystring)

        return response
