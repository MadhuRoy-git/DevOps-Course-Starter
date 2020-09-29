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

@mock.patch('requests.get')
def test_index_page(mock_get_requests, client):
    # Replace call to requests.get(url) with our own function
    mock_get_requests.side_effect = mock_get_cards

    response = client.get('/')
    assert response.status_code == 200
    assert response.headers['Content-Type'] == "text/html; charset=utf-8"

def mock_get_cards(url, params):
    data = {
        "id": "5f3aa16af331a53956b9b290",
        "checkItemStates": null,
        "closed": false,
        "dateLastActivity": "2020-08-18T12:34:10.753Z",
        "desc": "",
        "descData": null,
        "dueReminder": null,
        "idBoard": "5f3a9a92b421455eaa2ca174",
        "idList": "5f3a9d90546f2731c72baf4c",
        "idMembersVoted": [],
        "idShort": 1,
        "idAttachmentCover": null,
        "idLabels": [],
        "manualCoverAttachment": false,
        "name": "MadhuCard1",
        "pos": 16384,
        "shortLink": "kZtTeD26",
        "isTemplate": false,
        "badges": {
            "attachmentsByType": {
                "trello": {
                    "board": 0,
                    "card": 0
                }
            },
            "location": false,
            "votes": 0,
            "viewingMemberVoted": false,
            "subscribed": false,
            "fogbugz": "",
            "checkItems": 0,
            "checkItemsChecked": 0,
            "checkItemsEarliestDue": null,
            "comments": 0,
            "attachments": 0,
            "description": false,
            "due": null,
            "dueComplete": false,
            "start": null
        },
        "dueComplete": false,
        "due": null,
        "idChecklists": [],
        "idMembers": [],
        "labels": [],
        "shortUrl": "https://trello.com/c/kZtTeD26",
        "start": null,
        "subscribed": false,
        "url": "https://trello.com/c/kZtTeD26/1-madhucard1",
        "cover": {
            "idAttachment": null,
            "color": null,
            "idUploadedBackground": null,
            "size": "normal",
            "brightness": "light"
        }
    },
    {
        "id": "5f453af6145c0c372658f127",
        "checkItemStates": null,
        "closed": false,
        "dateLastActivity": "2020-08-25T16:23:18.486Z",
        "desc": "Singing",
        "descData": null,
        "dueReminder": null,
        "idBoard": "5f3a9a92b421455eaa2ca174",
        "idList": "5f3a9a92b421455eaa2ca175",
        "idMembersVoted": [],
        "idShort": 6,
        "idAttachmentCover": null,
        "idLabels": [],
        "manualCoverAttachment": false,
        "name": "Song To Do",
        "pos": 6,
        "shortLink": "kwbVNxfO",
        "isTemplate": false,
        "badges": {
            "attachmentsByType": {
                "trello": {
                    "board": 0,
                    "card": 0
                }
            },
            "location": false,
            "votes": 0,
            "viewingMemberVoted": false,
            "subscribed": false,
            "fogbugz": "",
            "checkItems": 0,
            "checkItemsChecked": 0,
            "checkItemsEarliestDue": null,
            "comments": 0,
            "attachments": 0,
            "description": true,
            "due": null,
            "dueComplete": false,
            "start": null
        },
        "dueComplete": false,
        "due": null,
        "idChecklists": [],
        "idMembers": [],
        "labels": [],
        "shortUrl": "https://trello.com/c/kwbVNxfO",
        "start": null,
        "subscribed": false,
        "url": "https://trello.com/c/kwbVNxfO/6-song-to-do",
        "cover": {
            "idAttachment": null,
            "color": null,
            "idUploadedBackground": null,
            "size": "normal",
            "brightness": "light"
        }
    },
    {
        "id": "5f43eb33e45b614330dad28b",
        "checkItemStates": null,
        "closed": false,
        "dateLastActivity": "2020-08-25T16:41:04.719Z",
        "desc": "",
        "descData": null,
        "dueReminder": null,
        "idBoard": "5f3a9a92b421455eaa2ca174",
        "idList": "5f3a9a92b421455eaa2ca175",
        "idMembersVoted": [],
        "idShort": 3,
        "idAttachmentCover": null,
        "idLabels": [],
        "manualCoverAttachment": false,
        "name": "Shopping To Do",
        "pos": 65535,
        "shortLink": "NIYwy65J",
        "isTemplate": false,
        "badges": {
            "attachmentsByType": {
                "trello": {
                    "board": 0,
                    "card": 0
                }
            },
            "location": false,
            "votes": 0,
            "viewingMemberVoted": false,
            "subscribed": false,
            "fogbugz": "",
            "checkItems": 0,
            "checkItemsChecked": 0,
            "checkItemsEarliestDue": null,
            "comments": 0,
            "attachments": 0,
            "description": false,
            "due": null,
            "dueComplete": false,
            "start": null
        },
        "dueComplete": false,
        "due": null,
        "idChecklists": [],
        "idMembers": [],
        "labels": [],
        "shortUrl": "https://trello.com/c/NIYwy65J",
        "start": null,
        "subscribed": false,
        "url": "https://trello.com/c/NIYwy65J/3-shopping-to-do",
        "cover": {
            "idAttachment": null,
            "color": null,
            "idUploadedBackground": null,
            "size": "normal",
            "brightness": "light"
        }
    },
    {
        "id": "5f43eb3fe37c5947d732db8f",
        "checkItemStates": null,
        "closed": false,
        "dateLastActivity": "2020-08-24T16:30:55.261Z",
        "desc": "",
        "descData": null,
        "dueReminder": null,
        "idBoard": "5f3a9a92b421455eaa2ca174",
        "idList": "5f3a9a92b421455eaa2ca175",
        "idMembersVoted": [],
        "idShort": 4,
        "idAttachmentCover": null,
        "idLabels": [],
        "manualCoverAttachment": false,
        "name": "Homework To Do",
        "pos": 131071,
        "shortLink": "InJW6Q31",
        "isTemplate": false,
        "badges": {
            "attachmentsByType": {
                "trello": {
                    "board": 0,
                    "card": 0
                }
            },
            "location": false,
            "votes": 0,
            "viewingMemberVoted": false,
            "subscribed": false,
            "fogbugz": "",
            "checkItems": 0,
            "checkItemsChecked": 0,
            "checkItemsEarliestDue": null,
            "comments": 0,
            "attachments": 0,
            "description": false,
            "due": null,
            "dueComplete": false,
            "start": null
        },
        "dueComplete": false,
        "due": null,
        "idChecklists": [],
        "idMembers": [],
        "labels": [],
        "shortUrl": "https://trello.com/c/InJW6Q31",
        "start": null,
        "subscribed": false,
        "url": "https://trello.com/c/InJW6Q31/4-homework-to-do",
        "cover": {
            "idAttachment": null,
            "color": null,
            "idUploadedBackground": null,
            "size": "normal",
            "brightness": "light"
        }
    },
    {
        "id": "5f6ccf4b02db0d21e0c949c0",
        "checkItemStates": null,
        "closed": false,
        "dateLastActivity": "2020-09-24T17:06:13.254Z",
        "desc": "Studying",
        "descData": null,
        "dueReminder": null,
        "idBoard": "5f3a9a92b421455eaa2ca174",
        "idList": "5f3a9a92b421455eaa2ca176",
        "idMembersVoted": [],
        "idShort": 9,
        "idAttachmentCover": null,
        "idLabels": [],
        "manualCoverAttachment": false,
        "name": "Studies",
        "pos": 9,
        "shortLink": "IAEtpqRT",
        "isTemplate": false,
        "badges": {
            "attachmentsByType": {
                "trello": {
                    "board": 0,
                    "card": 0
                }
            },
            "location": false,
            "votes": 0,
            "viewingMemberVoted": false,
            "subscribed": false,
            "fogbugz": "",
            "checkItems": 0,
            "checkItemsChecked": 0,
            "checkItemsEarliestDue": null,
            "comments": 0,
            "attachments": 0,
            "description": true,
            "due": null,
            "dueComplete": false,
            "start": null
        },
        "dueComplete": false,
        "due": null,
        "idChecklists": [],
        "idMembers": [],
        "labels": [],
        "shortUrl": "https://trello.com/c/IAEtpqRT",
        "start": null,
        "subscribed": false,
        "url": "https://trello.com/c/IAEtpqRT/9-studies",
        "cover": {
            "idAttachment": null,
            "color": null,
            "idUploadedBackground": null,
            "size": "normal",
            "brightness": "light"
        }
    },
    {
        "id": "5f43f022f4ee855e3664ea83",
        "checkItemStates": null,
        "closed": false,
        "dateLastActivity": "2020-08-25T16:46:17.971Z",
        "desc": "Cook the dinner",
        "descData": null,
        "dueReminder": null,
        "idBoard": "5f3a9a92b421455eaa2ca174",
        "idList": "5f3a9a92b421455eaa2ca177",
        "idMembersVoted": [],
        "idShort": 5,
        "idAttachmentCover": null,
        "idLabels": [],
        "manualCoverAttachment": false,
        "name": "Cooking To Do",
        "pos": 5,
        "shortLink": "r4283PA1",
        "isTemplate": false,
        "badges": {
            "attachmentsByType": {
                "trello": {
                    "board": 0,
                    "card": 0
                }
            },
            "location": false,
            "votes": 0,
            "viewingMemberVoted": false,
            "subscribed": false,
            "fogbugz": "",
            "checkItems": 0,
            "checkItemsChecked": 0,
            "checkItemsEarliestDue": null,
            "comments": 0,
            "attachments": 0,
            "description": true,
            "due": null,
            "dueComplete": false,
            "start": null
        },
        "dueComplete": false,
        "due": null,
        "idChecklists": [],
        "idMembers": [],
        "labels": [],
        "shortUrl": "https://trello.com/c/r4283PA1",
        "start": null,
        "subscribed": false,
        "url": "https://trello.com/c/r4283PA1/5-cooking-to-do",
        "cover": {
            "idAttachment": null,
            "color": null,
            "idUploadedBackground": null,
            "size": "normal",
            "brightness": "light"
        }
    },
    {
        "id": "5f453c54311af356f5fd2c6b",
        "checkItemStates": null,
        "closed": false,
        "dateLastActivity": "2020-09-24T17:06:35.673Z",
        "desc": "Dancing",
        "descData": null,
        "dueReminder": null,
        "idBoard": "5f3a9a92b421455eaa2ca174",
        "idList": "5f3a9a92b421455eaa2ca177",
        "idMembersVoted": [],
        "idShort": 7,
        "idAttachmentCover": null,
        "idLabels": [],
        "manualCoverAttachment": false,
        "name": "Dance To Do",
        "pos": 7,
        "shortLink": "qRxSHV2R",
        "isTemplate": false,
        "badges": {
            "attachmentsByType": {
                "trello": {
                    "board": 0,
                    "card": 0
                }
            },
            "location": false,
            "votes": 0,
            "viewingMemberVoted": false,
            "subscribed": false,
            "fogbugz": "",
            "checkItems": 0,
            "checkItemsChecked": 0,
            "checkItemsEarliestDue": null,
            "comments": 0,
            "attachments": 0,
            "description": true,
            "due": null,
            "dueComplete": false,
            "start": null
        },
        "dueComplete": false,
        "due": null,
        "idChecklists": [],
        "idMembers": [],
        "labels": [],
        "shortUrl": "https://trello.com/c/qRxSHV2R",
        "start": null,
        "subscribed": false,
        "url": "https://trello.com/c/qRxSHV2R/7-dance-to-do",
        "cover": {
            "idAttachment": null,
            "color": null,
            "idUploadedBackground": null,
            "size": "normal",
            "brightness": "light"
        }
    },
    {
        "id": "5f453e3261b9dd3e31702490",
        "checkItemStates": null,
        "closed": false,
        "dateLastActivity": "2020-08-25T16:37:19.881Z",
        "desc": "Groceries",
        "descData": null,
        "dueReminder": null,
        "idBoard": "5f3a9a92b421455eaa2ca174",
        "idList": "5f3a9a92b421455eaa2ca177",
        "idMembersVoted": [],
        "idShort": 8,
        "idAttachmentCover": null,
        "idLabels": [],
        "manualCoverAttachment": false,
        "name": "Groceries To Do",
        "pos": 8,
        "shortLink": "JDUDAB9a",
        "isTemplate": false,
        "badges": {
            "attachmentsByType": {
                "trello": {
                    "board": 0,
                    "card": 0
                }
            },
            "location": false,
            "votes": 0,
            "viewingMemberVoted": false,
            "subscribed": false,
            "fogbugz": "",
            "checkItems": 0,
            "checkItemsChecked": 0,
            "checkItemsEarliestDue": null,
            "comments": 0,
            "attachments": 0,
            "description": true,
            "due": null,
            "dueComplete": false,
            "start": null
        },
        "dueComplete": false,
        "due": null,
        "idChecklists": [],
        "idMembers": [],
        "labels": [],
        "shortUrl": "https://trello.com/c/JDUDAB9a",
        "start": null,
        "subscribed": false,
        "url": "https://trello.com/c/JDUDAB9a/8-groceries-to-do",
        "cover": {
            "idAttachment": null,
            "color": null,
            "idUploadedBackground": null,
            "size": "normal",
            "brightness": "light"
        }
    },
    {
        "id": "5f3bcc1a96d8747bfc177517",
        "checkItemStates": null,
        "closed": false,
        "dateLastActivity": "2020-08-18T12:47:23.253Z",
        "desc": "",
        "descData": null,
        "dueReminder": null,
        "idBoard": "5f3a9a92b421455eaa2ca174",
        "idList": "5f3a9a92b421455eaa2ca177",
        "idMembersVoted": [],
        "idShort": 2,
        "idAttachmentCover": null,
        "idLabels": [],
        "manualCoverAttachment": false,
        "name": "Original To Do Card",
        "pos": 65535,
        "shortLink": "Sgb0yy2U",
        "isTemplate": false,
        "badges": {
            "attachmentsByType": {
                "trello": {
                    "board": 0,
                    "card": 0
                }
            },
            "location": false,
            "votes": 0,
            "viewingMemberVoted": false,
            "subscribed": false,
            "fogbugz": "",
            "checkItems": 0,
            "checkItemsChecked": 0,
            "checkItemsEarliestDue": null,
            "comments": 0,
            "attachments": 0,
            "description": false,
            "due": null,
            "dueComplete": false,
            "start": null
        },
        "dueComplete": false,
        "due": null,
        "idChecklists": [],
        "idMembers": [],
        "labels": [],
        "shortUrl": "https://trello.com/c/Sgb0yy2U",
        "start": null,
        "subscribed": false,
        "url": "https://trello.com/c/Sgb0yy2U/2-original-to-do-card",
        "cover": {
            "idAttachment": null,
            "color": null,
            "idUploadedBackground": null,
            "size": "normal",
            "brightness": "light"
        }
    }
    if url == f'https://api.trello.com/1/boards/5f3a9a92b421455eaa2ca174/cards':
        response = Mock()
        # sample_trello_lists_response should point to some test response data
        response.json.return_value = data
        return response
    return None
 