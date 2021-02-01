import requests
from requests import Response
from typing import Union, List
import os

SIG_API_URL = os.environ.get("SIG_API_URL", "http://localhost:8083")
SIG_API_KEY = os.environ.get("SIG_API_KEY", "http://localhost:8083")


class SigApiAdapter:

    @staticmethod
    def textual_search(query: str, limit: int = 5) -> Response:

        url = f"{SIG_API_URL}/recherche-localisation/textuelle"

        querystring = {"q": query, "type": "municipality", "limit": str(limit)}

        headers = {
            'x-api-key': SIG_API_KEY,
        }

        response = requests.request("GET", url, headers=headers, params=querystring)

        return response

    @staticmethod
    def code_territory_search(postal_code: Union[str, List[str]],
                              insee_code: Union[str, List[str]],
                              code_dept: Union[str, List[str]]) -> Response:
        url = f"{SIG_API_URL}/decoupage-administratif/territoire/codes"

        querystring = {"codesInsee": insee_code,
                       "codesPostaux": postal_code,
                       "codesDept": code_dept
                       }

        headers = {
            'x-api-key': SIG_API_KEY
        }

        response = requests.request("GET", url, headers=headers, params=querystring)

        return response
