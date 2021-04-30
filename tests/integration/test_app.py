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
        "board_id": "board1",
        "list_name": "todolist",
        "cards": {
                "card_id": "card1",
                "card_name": "Shopping",
                "card_desc": "Groceries to do",
                "card_dateLastActivity": "2020-08-19T14:09:28.403Z"
            }
    },
    {
        "board_id": "board1",
        "list_name": "todolist",
        "cards": {
                "card_id": "card2",
                "card_name": "Music",
                "card_desc": "Singing to do",
                "card_dateLastActivity": "2020-07-19T14:09:28.403Z"
            }
    }
]

@pytest.fixture
def client():
    # Use our test integration config instead of the 'real' version 
    with mongomock.patch(servers=(('server.example.com', 27017),)):
        file_path = find_dotenv('.env.test')
        load_dotenv(file_path, override=True)
        # Create the new app.
        test_app, collection = create_app()
        # Use the app to create a test_client that can be used in our tests.
        with test_app.test_client() as client: 
            yield client

@mongomock.patch(servers=(('server.example.com', 27017),))
def test_index_page(client):
    dbclient = pymongo.MongoClient('server.example.com')
    dbclient.TodoListDB.todos.insert_many(test_todos)

    response = client.get('/')

    assert response.status_code == 200
    assert response.headers['Content-Type'] == 'text/html; charset=utf-8'
