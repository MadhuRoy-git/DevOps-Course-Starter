import pytest
import os
from threading import Thread
import requests
import db_items as mongo
from app import create_app
from flask import current_app as app
from dotenv import load_dotenv, find_dotenv
from selenium import webdriver

@pytest.fixture(scope='module')
def test_app():
    # Update the board id environment variable
    file_path = find_dotenv('.env')
    load_dotenv(file_path, override=True)

    os.environ['BOARD_ID'] = 'test_board_id'

    # construct the new application
    application, collection = create_app() 
    application.config['LOGIN_DISABLED'] = True
    
    # start the app in its own thread.
    thread = Thread(target=lambda: application.run(use_reloader=False)) 
    thread.daemon = True
    thread.start()
    yield app
    # Tear Down
    thread.join(1) 
    delete_board(collection)

# THIS IS USED TO RUN THE E2E TESTS IN DOCKER CONTAINER
@pytest.fixture(scope='module') 
def driver():
    opts = webdriver.ChromeOptions()
    opts.add_argument('--headless') 
    opts.add_argument('--no-sandbox') 
    with webdriver.Chrome('/usr/bin/chromedriver', options=opts) as driver:
        yield driver

# UNCOMMENT THIS TO RUN THE E2E TESTS LOCALLY - COMMENT THE ABOVE
# @pytest.fixture(scope='module') 
# def driver():
#     with webdriver.Firefox() as driver:
#         yield driver

def test_task_journey(driver, test_app): 
    driver.get('http://0.0.0.0:5000/')
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
    assert driver.find_element_by_id("todostatus").text == "todo"

    #Start item
    driver.find_element_by_id("start-btn").click()
    driver.implicitly_wait(2)
    assert driver.find_element_by_id("doingname").text == todo_title
    assert driver.find_element_by_id("doingdesc").text == todo_desc
    assert driver.find_element_by_id("doingstatus").text == "doing"

    #Complete item
    driver.find_element_by_id("complete-btn").click()
    driver.implicitly_wait(2)
    assert driver.find_element_by_id("donename").text == todo_title
    assert driver.find_element_by_id("donedesc").text == todo_desc
    assert driver.find_element_by_id("donestatus").text == "done"

    #Undo item
    driver.find_element_by_id("undo-btn").click()
    driver.implicitly_wait(2)
    assert driver.find_element_by_id("todoname").text == todo_title
    assert driver.find_element_by_id("tododesc").text == todo_desc
    assert driver.find_element_by_id("todostatus").text == "todo"

def delete_board(collection):
    """
    Deletes the board at the end of the test.
    """
    collection.delete_many( { 'board_id': 'test_board_id' } )

