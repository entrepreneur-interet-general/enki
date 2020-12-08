from typing import List

from ....adapters.http.nexsis.sig_api import SigApiAdapter
from .textual_search_municipality import SearchMunicipalityEntity


class MunicipalityTextualSearchService:
    @staticmethod
    def list_cities_by_query(query: str) -> List[SearchMunicipalityEntity]:
        response = SigApiAdapter.textual_search(query=query)
        data = response.json()
        return [SearchMunicipalityEntity(**res).to_dict() for res in data]
