import pytest
import os
from threading import Thread
import requests
from app import create_app
from flask import current_app as app
from dotenv import load_dotenv, find_dotenv
from selenium import webdriver

@pytest.fixture(scope='module')
def test_app():
    # Create the new board & update the board id environment variable
    file_path = find_dotenv('.env')
    load_dotenv(file_path, override=True)

    # construct the new application
    application = create_app()
    board_id = create_trello_board('My E2E Test Board')
    os.environ['boardId'] = board_id
    
    # start the app in its own thread.
    thread = Thread(target=lambda: application.run(use_reloader=False)) 
    thread.daemon = True
    thread.start()
    yield app
    # Tear Down
    thread.join(1) 
    delete_trello_board(board_id)

@pytest.fixture(scope='module')
def driver():
    with webdriver.Firefox() as driver:
        yield driver

def test_task_journey(driver, test_app): 
    driver.get('http://localhost:5000/')
    assert driver.title == 'To-Do App'

def create_trello_board(name):
    """
    Creates a new board with given name.
    Returns:
        The id of the newly created board.
    """
    url = "https://api.trello.com/1/boards"
    query = {
        'key': app.config['KEY'],
        'token': app.config['TOKEN'],
        'name': name
    }
    response = requests.request("POST", url, params=query)
    return response.json()['id']


def delete_trello_board(board_id):
    """
    Deletes a board with given id. Returns nothing.
    """
    url = "https://api.trello.com/1/boards/{}".format(board_id)
    query = {
        'key': app.config['KEY'],
        'token': app.config['TOKEN']
    }
    requests.request("DELETE", url, params=query)