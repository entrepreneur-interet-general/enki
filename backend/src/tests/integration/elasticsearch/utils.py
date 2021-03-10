import json

from elasticsearch import Elasticsearch


def create_index(client: Elasticsearch, index_name: str, template_path: str):
    from pathlib import Path
    p = Path(__file__).resolve().parent / template_path
    with p.open() as f:
        mapping = json.load(f)
    response = client.indices.create(
        index=index_name,
        body=mapping,
        ignore=400  # ignore 400 already exists code
    )
    return response
