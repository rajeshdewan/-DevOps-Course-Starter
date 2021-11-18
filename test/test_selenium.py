import pytest
from selenium import webdriver
from todo_app.data.session_items import create_trello_board,delete_trello_board
from threading import Thread
from todo_app.app import create_app
import time

import os

@pytest.fixture(scope='module')
def driver():
   opts = webdriver.ChromeOptions()
   opts.add_argument('--headless')
   opts.add_argument('--no-sandbox')
   opts.add_argument('--disable-dev-shm-usage')
   with webdriver.Chrome(options=opts) as driver:
      yield driver

@pytest.fixture(scope='module')
def app_with_temp_board():
 # Create the new board & update the board idenvironment variable
   board_id = create_trello_board()
   os.environ['TRELLO_BOARD_ID'] = board_id[0]
   
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
    time.sleep(5)
    assert driver.title == 'To-Do App'

def test_new_card(driver,app_with_temp_board):
   driver.get('http://localhost:5000')
   new_card_title_box = driver.find_element_by_name('itemname')
   new_card_title_box.send_keys("module3")
   submit_new_card_button = driver.find_element_by_id('addbutton')
   submit_new_card_button.click()
   new_todo = driver.find_element_by_name("itemname").text
   assert new_todo is not None