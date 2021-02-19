import pytest
import os
from threading import Thread
import requests
import trello_items as trello
from app import create_app
from flask import current_app as app
from dotenv import load_dotenv, find_dotenv
from selenium import webdriver

@pytest.fixture(scope='module')
def test_app():
    # Create the new board & update the board id environment variable
    file_path = find_dotenv('.env')
    load_dotenv(file_path, override=True)
    
    board_id = create_trello_board('My E2E Test Board')
    update_env_vars(board_id)

    # construct the new application
    application = create_app()
    
    # start the app in its own thread.
    thread = Thread(target=lambda: application.run(use_reloader=False)) 
    thread.daemon = True
    thread.start()
    yield app
    # Tear Down
    thread.join(1) 
    delete_trello_board(board_id)

# THIS IS USED TO RUN THE E2E TESTS IN DOCKER CONTAINER
@pytest.fixture(scope='module') 
def driver():
    opts = webdriver.ChromeOptions()
    opts.add_argument('--headless') 
    opts.add_argument('--no-sandbox') 
    with webdriver.Chrome('./chromedriver', options=opts) as driver:
        yield driver

# UNCOMMENT THIS TO RUN THE E2E TESTS LOCALLY - COMMENT THE ABOVE
# @pytest.fixture(scope='module') 
# def driver():
#     with webdriver.Firefox() as driver:
#         yield driver

def update_env_vars(board_id):
    os.environ['boardId'] = board_id
    lists = trello.get_all_lists_on_board(board_id)
    for list in lists:
        if list['name'] == 'To Do':
            os.environ['TODO_LIST_ID'] = list['id']
        elif list['name'] == 'Doing':
            os.environ['DOING_LIST_ID'] = list['id']
        else:
            os.environ['DONE_LIST_ID'] = list['id']

def test_task_journey(driver, test_app): 
    driver.get('http://127.0.0.1:5000/')
    assert driver.title == 'To-Do App'

    todo_title = "Watch movie"
    todo_desc = "Movie on TV"

    # Create new item
    els = driver.find_elements_by_tag_name("td")
    driver.find_element_by_id("name_input").send_keys(todo_title)
    driver.find_element_by_id("desc_input").send_keys(todo_desc)
    driver.find_element_by_id("add-item").click()
    driver.implicitly_wait(2)
    els = driver.find_elements_by_tag_name("td")
    assert driver.find_element_by_id("todoname").text == todo_title
    assert driver.find_element_by_id("tododesc").text == todo_desc
    assert driver.find_element_by_id("todostatus").text == "To Do"

    #Start item
    driver.find_element_by_id("start-btn").click()
    driver.implicitly_wait(2)
    assert driver.find_element_by_id("doingname").text == todo_title
    assert driver.find_element_by_id("doingdesc").text == todo_desc
    assert driver.find_element_by_id("doingstatus").text == "Doing"

    #Complete item
    driver.find_element_by_id("complete-btn").click()
    driver.implicitly_wait(2)
    assert driver.find_element_by_id("donename").text == todo_title
    assert driver.find_element_by_id("donedesc").text == todo_desc
    assert driver.find_element_by_id("donestatus").text == "Done"

    #Undo item
    driver.find_element_by_id("undo-btn").click()
    driver.implicitly_wait(2)
    assert driver.find_element_by_id("todoname").text == todo_title
    assert driver.find_element_by_id("tododesc").text == todo_desc
    assert driver.find_element_by_id("todostatus").text == "To Do"


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