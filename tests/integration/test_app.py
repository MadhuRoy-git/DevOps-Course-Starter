import pytest
import db_items as mongoDB
import os
import pymongo
from unittest import mock
from unittest.mock import Mock
from app import create_app
from dotenv import load_dotenv, find_dotenv

# FILE NEEDS TO BE CHANGED AFTER LEARNING ABOUT MONGOMOCK

@pytest.fixture
def client():
    # Use our test integration config instead of the 'real' version 
    file_path = find_dotenv('.env.test')
    load_dotenv(file_path, override=True)
    # Create the new app.
    test_app, collection = create_app()
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
    data = [{'_id': ObjectId('60747cb18817b98e218e847e'),
            'board_id': 'TestBoard123',
            'cards': {'card_dateLastActivity': '2021-04-12',
                        'card_desc': 'Writing a song',
                        'card_id': '08863bed-0dfc-4b2c-bcb3-000c8cd633be',
                        'card_name': 'Song'},
            'list_name': 'doing'},
            {'_id': ObjectId('60747d29bd190dc8950efb82'),
            'board_id': 'TestBoard123',
            'cards': {'card_dateLastActivity': '2021-04-12',
                        'card_desc': 'Studying',
                        'card_id': '2',
                        'card_name': 'Study'},
            'list_name': 'doing'}]

 
    if method == mongoDB.get_list(collection,'TestBoard123','doing'):
        response = Mock()
        # sample_trello_lists_response should point to some test response data
        response.json.return_value = data
        return response

    return None
 