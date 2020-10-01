import pytest
import os
from threading import Thread
import requests
import time
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
    print("board_id =", board_id)
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
    driver.get('http://127.0.0.1:5000/')
    assert driver.title == 'To-Do App'

    # Create new item
    els = driver.find_elements_by_tag_name("td")
    driver.find_element_by_id("name_input").send_keys("Watch movie")
    driver.find_element_by_id("desc_input").send_keys("Movie on TV")
    driver.find_element_by_id("add-item").click()
    time.sleep(2)
    els = driver.find_elements_by_tag_name("td")
    assert driver.find_element_by_xpath("//td[2]").text == "Movie on TV"
    assert driver.find_element_by_xpath("//td[4]").text == "To Do"

    #Start item
    driver.find_element_by_id("start-btn").click()
    time.sleep(2)
    assert driver.find_element_by_xpath("//td[2]").text == "Movie on TV"
    assert driver.find_element_by_xpath("//td[4]").text == "Doing"

    #Complete item
    driver.find_element_by_id("complete-btn").click()
    time.sleep(2)
    assert driver.find_element_by_xpath("//td[2]").text == "Movie on TV"
    assert driver.find_element_by_xpath("//td[4]").text == "Done"


def create_trello_board(name):
    """
    Creates a new board with given name.
    Returns:
        The id of the newly created board.
    """
    url = "https://api.trello.com/1/boards"
    query = {
        'key': os.getenv('apiKey'),
        'token': os.getenv('apiToken'),
        'name': name
    }
    response = requests.request("POST", url, params=query)
    print("board_id in create trello board function =", response.json()['id'])
    return response.json()['id']


def delete_trello_board(board_id):
    """
    Deletes a board with given id. Returns nothing.
    """
    url = "https://api.trello.com/1/boards/{}".format(board_id)
    query = {
        'key': os.getenv('apiKey'),
        'token': os.getenv('apiToken')
    }
    requests.request("DELETE", url, params=query)