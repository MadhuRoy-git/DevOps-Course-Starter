import pytest
from unittest import mock
from unittest.mock import Mock
from app import create_app
from dotenv import load_dotenv, find_dotenv

@pytest.fixture
def client():
    # Use our test integration config instead of the 'real' version 
    file_path = find_dotenv('.env.test')
    load_dotenv(file_path, override=True)
    # Create the new app.
    test_app = create_app()
    # Use the app to create a test_client that can be used in our tests.
    with test_app.test_client() as client: 
        yield client

@mock.patch('requests.request')
def test_index_page(mock_get_requests, client):
    # Replace call to requests.get(url) with our own function
    mock_get_requests.side_effect = mock_request

    response = client.get('/')
    assert response.status_code == 200
    assert response.headers['Content-Type'] == "text/html; charset=utf-8"

def mock_request(method, url, params):
    data = [{
        "id": "5f3aa16af331a53956b9b290",
        "checkItemStates": "TestStatus",
        "closed": "false",
        "dateLastActivity": "2020-08-18T12:34:10.753Z",
        "desc": "",
        "descData": "null",
        "dueReminder": "null",
        "idBoard": "5f3a9a92b421455eaa2ca174",
        "idList": "5f3a9d90546f2731c72baf4c",
        "idMembersVoted": [],
        "idShort": 1,
        "idAttachmentCover": "null",
        "idLabels": [],
        "manualCoverAttachment": "false",
        "name": "MadhuCard1",
        "pos": 16384,
        "shortLink": "kZtTeD26",
        "isTemplate": "false",
        "badges": {
            "attachmentsByType": {
                "trello": {
                    "board": 0,
                    "card": 0
                }
            },
            "location": "false",
            "votes": 0,
            "viewingMemberVoted": "false",
            "subscribed": "false",
            "fogbugz": "",
            "checkItems": 0,
            "checkItemsChecked": 0,
            "checkItemsEarliestDue": "null",
            "comments": 0,
            "attachments": 0,
            "description": "false",
            "due": "null",
            "dueComplete": "false",
            "start": "null"
        },
        "dueComplete": "false",
        "due": "null",
        "idChecklists": [],
        "idMembers": [],
        "labels": [],
        "shortUrl": "https://trello.com/c/kZtTeD26",
        "start": "null",
        "subscribed": "false",
        "url": "https://trello.com/c/kZtTeD26/1-madhucard1",
        "cover": {
            "idAttachment": "null",
            "color": "null",
            "idUploadedBackground": "null",
            "size": "normal",
            "brightness": "light"
        }
    }]

    list = {
        "id": "5f3a9d90546f2731c72baf4c",
        "name": "MadhuList",
        "closed": "false",
        "pos": 8192,
        "softLimit": "null",
        "creationMethod": "null",
        "idBoard": "5f3a9a92b421455eaa2ca174",
        "limits": {
            "cards": {
                "openPerList": {
                    "status": "ok",
                    "disableAt": 5000,
                    "warnAt": 4500
                },
                "totalPerList": {
                    "status": "ok",
                    "disableAt": 1000000,
                    "warnAt": 900000
                }
            }
        },
        "subscribed": "false"
    }

    if url == f'https://api.trello.com/1/boards/board1234/cards':
        response = Mock()
        # sample_trello_lists_response should point to some test response data
        response.json.return_value = data
        return response
    if url == f'https://api.trello.com/1/cards/5f3aa16af331a53956b9b290/list':
        response = Mock()
        # sample_trello_lists_response should point to some test response data
        response.json.return_value = list
        return response
    return None
 