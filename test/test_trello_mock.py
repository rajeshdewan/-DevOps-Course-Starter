import json
from todo_app.app import create_app
from dotenv import load_dotenv,find_dotenv
import pytest
from unittest.mock import patch,Mock

@pytest.fixture
def client():
 # Use our test integration config instead of the 'real' version
    file_path = find_dotenv('.env.test')
    load_dotenv(file_path, override=True)
    # Create the new app.
    test_app = create_app()
    # Use the app to create a test_client that can be used in ourtests.
    with test_app.test_client() as client:
        yield client

@patch('requests.request')
def test_index_page(mock_get_requests, client):
    mock_get_requests.side_effect = mock_get_lists
    response = client.get('/') ##pretending to make http req
#can be used to spy

def mock_get_lists(method, url, params):
    board_id = '100'
    todoid = '200'
    #if url == f'https://api.trello.com/1/boards/{TEST_BOARD_ID}/lists':
    if url == f'https://api.trello.com/1/members/me/boards':    
        response = Mock()
        response.text = '[{"id":"' +board_id +'"}]'
        #= json.dumps([{"id": board_id}])

        #response.json.return_value = "60be30080cacf2335dbaa61c Packing Not Started"
        return response
    elif url == 'https://api.trello.com/1/boards/'+board_id+'/lists': 
        response = Mock()
        response.text == json.dumps([{"id": todoid}])
        return response
    return None
    
    #assert response[0].get("name") == "Holiday"
# @patch('requests.get')
# def test_index_page(self,mock_get_requests, client):
#     mock_get_requests.return_value.status_code = 200
#     response = client.get('/')
#     assert response.status_code == 200
#     self.assertEqual(response.status_code, 200)

# def test_index_page(client):
#     response = client.get('/')
  
#  assert response.status_code == 200
