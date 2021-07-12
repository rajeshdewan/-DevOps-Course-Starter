import pytest
from selenium import webdriver
import os
@pytest.fixture(scope='module')
def driver():
 # path to your webdriver download
    with webdriver.Chrome('./chromedriver') as driver:
        yield driver
def test_python_home(driver):
    driver.get("https://www.python.org")
    assert driver.title == 'Welcome to Python.org'


def test_downloads_page(driver):
 driver.get("https://www.python.org")
 link = driver.find_element_by_link_text('Downloads')
 link.click()
 assert driver.current_url == 'https://www.python.org/downloads/'


#test_lambdatest_todo_app():
# driver = webdriver.Chrome('./chromedriver')
# driver.get("https://www.python.org")
# print(driver.title)
