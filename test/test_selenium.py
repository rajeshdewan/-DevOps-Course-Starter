import pytest
from selenium import webdriver
from todo_app.data.session_items import create_trello_board,delete_trello_board
from threading import Thread
from todo_app.app import create_app

import os
@pytest.fixture(scope='module')
def driver():
 # path to your webdriver download
    with webdriver.Chrome('./chromedriver') as driver:
        yield driver


@pytest.fixture(scope='module')
def app_with_temp_board():
 # Create the new board & update the board idenvironment variable
   board_id = create_trello_board()
   os.environ['TRELLO_BOARD_ID'] = board_id
# construct the new application
   application = create_app()

# start the app in its own thread.
   thread = Thread(target=lambda:
   application.run(use_reloader=False))
   thread.daemon = True
   thread.start()
   yield application

   # Tear Down
   thread.join(1)
   delete_trello_board()

def test_task_journey(driver, app_with_temp_board):
    driver.get('http://localhost:5000/')
    assert driver.title == 'To-Do App'