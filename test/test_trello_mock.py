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
    response = client.get('/') 
    assert response.status_code == 200

@patch('requests.request')
def test_index_page1(mock_get_requests, client):
    mock_get_requests.side_effect = mock_get_lists
    response = client.get('/') 
    assert 'Not Started' in response.data.decode()

def mock_get_lists(method, url, params):
    board_id =  '60be2f051818be2e6b13fc78'
    todoid = '200'
    list_id ='200'
    list_id_done = '300'
    #if url == f'https://api.trello.com/1/boards/{TEST_BOARD_ID}/lists':
    if url == f'https://api.trello.com/1/members/me/boards':    
        response = Mock()
        response.text = '[{"id":"' +board_id +'"}]'


        return response
    elif url == 'https://api.trello.com/1/boards/'+board_id+'/lists': 
        response = Mock()
        response.text = json.dumps([{"id":"200","name": "To Do"},{"id":"300","name": "Done"}])

        return response
    elif url == 'https://api.trello.com/1/lists/'+list_id+'/cards':
        response= Mock()
        response.text = json.dumps([{"id":"400","name": "Not Started"},{"id":"500","name": "Done"}])
        return response
    elif url == 'https://api.trello.com/1/lists/'+list_id_done+'/cards':
        response= Mock()
        response.text = json.dumps([{"id":"400","name": "Not Started"},{"id":"500","name": "Done"}])
        return response

    
    return None
    
