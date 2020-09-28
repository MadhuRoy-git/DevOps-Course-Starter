import pytest
import mock
import requests
from app import create_app
from dotenv import load_dotenv, find_dotenv

@pytest.fixture
def client():
    # Use our test integration config instead of the 'real' version 
    file_path = find_dotenv('.env.test')
    load_dotenv(file_path, override=True)
    # Create the new app.
    test_app = app.create_app()
    # Use the app to create a test_client that can be used in our tests.
    with test_app.test_client() as client: 
        yield client

def test_index_page2(mock_get_requests, client): 
    response = client.get('/')

@mock.patch('requests.request')
def test_index_page(self, mock_get):
    """test index root method"""
    # mock_resp = self._mock_response(content="ELEPHANTS")
    # mock_get.return_value = mock_resp

    response = client.get('/')
    assert response.status_code == 200
    assert response.headers['Content-Type'] == "text/html; charset=utf-8"
 