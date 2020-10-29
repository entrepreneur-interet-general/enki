from typing import Dict
from flask.testing import FlaskClient
from entrypoints.flask_app import app
from ..utils.filter import filter_dict_with_keys

BASE_PATH_TASK: str = "/api/enki/v1/tags"


def test_add_tag_then_recovers_it_and_recovers_all():
    with app.test_client() as client:
        client: FlaskClient

        tag1 = {
            "uuid": "uuid_1",
            "title": "My e2e title",
            "description": "My e2e description"
        }
        add_tag_response = post_add_tag(client, tag1)

        assert add_tag_response.status_code == 201
        assert add_tag_response.json['message'] == "Success"

        # fetching added tag
        fetched_tag1_response = client.get(BASE_PATH_TASK + "/" + tag1["uuid"])
        assert fetched_tag1_response.status_code == 200

        print(fetched_tag1_response.json)
        print(fetched_tag1_response.json["tag"])
        print(type(fetched_tag1_response.json["tag"]))
        assert filter_dict_with_keys(fetched_tag1_response.json["tag"], tag1) == tag1

        # adding extra tag
        tag2 = {
            "uuid": "uuid_2",
            "title": "My other e2e title",
            "description": "My e2e description"
        }
        post_add_tag(client, tag2)

        # fetching all tags
        fetched_all_tags_response = client.get(BASE_PATH_TASK)
        assert fetched_all_tags_response.status_code == 200
        assert [filter_dict_with_keys(tag, tag1) for tag in fetched_all_tags_response.json["tags"]] == [tag1, tag2]


def post_add_tag(client: FlaskClient, body: Dict[str, str]):
    return client.post(BASE_PATH_TASK, json=body)
