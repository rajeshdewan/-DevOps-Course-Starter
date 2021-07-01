
import requests
import os
import json
from dotenv import load_dotenv

#Class to define propoerties of item created in Trello 
class MyItem:
   def __init__(self,itemid,title,status):
        self.id = itemid
        self.title = title
        self.status = status
   
   def displayitem(self):
       print (self.id, self.title,self.status)
  
#loading environment variables for KEY,TOKEN to be used if functions are invoked without flask
load_dotenv()

#Get id of board created in Trello
def getBoardid():
   url_for_board = 'https://api.trello.com/1/members/me/boards'


   query = {
      'key': os.getenv('KEY'),
      'token': os.getenv('TOKEN')
   }

   response = requests.request(
      "GET",
      url_for_board,
      params=query
   )
   
   getBoardresponse = response.text
   getBoardresponse = json.loads(getBoardresponse)
   return getBoardresponse[0]["id"]


#########Get list id of To Do#########

def gettodolistid(board_id):
   
   url_for_lists = 'https://api.trello.com/1/boards/'+board_id+'/lists'
   
   query = {
      'key': os.getenv('KEY'),
      'token': os.getenv('TOKEN')
   }


   response = requests.request(
      "GET",
      url_for_lists,
      params=query
   )
   
   getListsresponse = response.text
   getListsresponse = json.loads(getListsresponse)
   
   getListsresponse = [x['id'] for x in getListsresponse if x['name'] == 'To Do']
   getListsresponse = getListsresponse[0]
   return getListsresponse

   
##############Get list id of done############

def getdonelistid(board_id):
   
   url_for_lists = 'https://api.trello.com/1/boards/'+board_id+'/lists'
   
   query = {
      'key': os.getenv('KEY'),
      'token': os.getenv('TOKEN')
   }

   response = requests.request(
      "GET",
      url_for_lists,
      params=query
   )
   
   getListsresponse = response.text
   getListsresponse = json.loads(getListsresponse)
   
   getListsresponse = [x['id'] for x in getListsresponse if x['name'] == 'Done']
   getListsresponse = getListsresponse[0]
   return getListsresponse


################Get Items on To do and Done list ####################### 
def getallitems ():
   board_id = getBoardid()
   todolistid = gettodolistid(board_id)
   donelistid = getdonelistid(board_id)

   return getToDoItems(todolistid,"Not Started") + getToDoItems(donelistid,"Done")

def getToDoItems(list_id, list_name): 
   
   url_for_todoitems = 'https://api.trello.com/1/lists/'+list_id+'/cards'
   
   query = {
      'key': os.getenv('KEY'),
      'token': os.getenv('TOKEN')
   }

   response = requests.request(
      "GET",
      url_for_todoitems,
      params=query
   )
   
   gettodoitems = response.text
   gettodoitems = json.loads(gettodoitems)

   result = []

   for item in gettodoitems:
      item1 = MyItem(item["id"],item["name"],list_name)
      disp = item1.displayitem()
      result.append(item1)
   return result
   
######Create a card on To do items list

def putToDoItems(newcardname):
   board_id = getBoardid()
   todolistid = gettodolistid(board_id)


   url_for_todoitems = 'https://api.trello.com/1/cards'
   
   query = {
      'key': os.getenv('KEY'),
      'token': os.getenv('TOKEN'),
      'idList': todolistid,
      'name' : newcardname

   }

   response = requests.request(
      "POST",
      url_for_todoitems,
      params=query
   )
   
   puttodoitems = response.text
   puttodoitems = json.loads(puttodoitems)
   
#####Mark an item complete i.e. move it from To Do to Done list######

def markcomplete(itemid):
   board_id = getBoardid()
   
   donelistid = getdonelistid(board_id)
   urlformarkcomplete = 'https://api.trello.com/1/cards/'+itemid

   headers = {
   "Accept": "application/json"
   }
   query = {
      'key': os.getenv('KEY'),
      'token': os.getenv('TOKEN'),
      'idList': donelistid      
   }
   response = requests.request(
      "PUT",
      urlformarkcomplete,
      headers=headers,
      params=query
   )
