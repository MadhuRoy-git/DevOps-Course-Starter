import pytest
import db_items as mongoDB
import os
import pymongo
import mongomock
from app import create_app
from dotenv import load_dotenv, find_dotenv
from unittest.mock import patch

test_todos = [
    {
        "id": "id1",
        "last_modified": "2020-08-19T14:09:28.403Z",
        "title": "Test item 1",
        "duedate": None
    },
    {
        "id": "id2",
        "last_modified": "2020-08-19T14:09:28.403Z",
        "title": "Test item 2",
        "duedate": None
    },
    {
        "id": "id3",
        "last_modified": "2020-08-19T14:09:28.403Z",
        "title": "Test item 3",
        "duedate": "2020-06-20T10:00:00.403Z"
    }
]

@pytest.fixture
def client():
    # Use our test integration config instead of the 'real' version 
    with mongomock.patch(servers=(('server.example.com'))):
        file_path = find_dotenv('.env.test')
        load_dotenv(file_path, override=True)
        # Create the new app.
        test_app, collection = create_app()
        # Use the app to create a test_client that can be used in our tests.
        with test_app.test_client() as client: 
            yield client

def test_index_page(client):
    client = pymongo.MongoClient('server.example.com')
    client.TodoListDB.todos.insert_many(test_todos)

    response = client.get('/')

    assert b"Test item 1" in response.data
    assert b"Test item 2" in response.data
    assert b"Test item 3" in response.data
    assert b"Jun 20" in response.data
