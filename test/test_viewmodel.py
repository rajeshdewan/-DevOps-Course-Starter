from todo_app.data.session_items import ViewModel,MyItem
from todo_app.app import create_app
from dotenv import load_dotenv,find_dotenv


def test_todo():
    item1 = MyItem('100','Weather','Not Started')
    item2 = MyItem('101','Transport','Done')
    x = ViewModel([item1,item2])

    todoitems1 = x.todoitems
    assert todoitems1 == [item1]




# import pytest
# @pytest.fixture
# def input_value():
#    input = 12
#    return input

# def test_divisible_by_3(input_value):
#    assert input_value % 3 == 0

# def test_divisible_by_6(input_value):
#    assert input_value % 6 == 0
# def test_uppercase():
#     assert "loud noises".upper() == "LOUD NoISES"

# import requests
# def test_request_response():
#     # Send a request to the API server and store the response.
#     response = requests.get('http://jsonplaceholder.typicode.com/todos')

#     # Confirm that the request-response cycle completed successfully.
#     assert response.status_code == 200