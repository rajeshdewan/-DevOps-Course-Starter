
import requests
import os
import json
from dotenv import load_dotenv
from threading import Thread

#Class to define propoerties of item created in Trello 
class MyItem:
   def __init__(self,itemid,title,status):
        self.id = itemid
        self.title = title
        self.status = status
   
   def displayitem(self):
       print (self.id, self.title,self.status)
  
class ViewModel:
   def __init__(self, items):
      self._items = items
   @property
   def items(self):
      return self._items
   @property
   def todoitems(self):
      listoftodo = []
      listofdone = []
      for i in self._items:
         if i.status == "Not Started":
            listoftodo.append(i)
      return listoftodo

   @property
   def doneitems(self):
      listofdone = []
      for i in self._items:
         if i.status == "Done":
            listofdone.append(i)
      return listofdone



#loading environment variables for KEY,TOKEN to be used if functions are invoked without flask
load_dotenv()


# def getBoardid():
#     return os.environ['TRELLO_BOARD_ID']

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


## Get items only on To Do list
def getonlytodoitems():
   board_id = getBoardid()
   todolistid = gettodolistid(board_id)
   return getToDoItems(todolistid,"Not Started")


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


#######Create a new board ######
def create_trello_board():
   url = "https://api.trello.com/1/boards/"



   query = {
      'key': os.getenv('KEY'),
      'token': os.getenv('TOKEN'),
      'name': 'Assignments'
   }


   response = requests.request(
      "POST",
      url,
      params=query
   )
   
   getresponse1 = response.json()
   idofboardcreated = getresponse1.get('id')
   nameofboardcreated = getresponse1.get('name')
   
   return idofboardcreated,nameofboardcreated
   



#######Delete the board ######

def delete_trello_board():
   #load_dotenv()
   idtobedeleted = os.getenv('TRELLO_BOARD_ID')
   
   url = f"https://api.trello.com/1/boards/{idtobedeleted}"
   
   query = {
      'key': os.getenv('KEY'),
      'token': os.getenv('TOKEN')      
   }
   response = requests.request(
   "DELETE",
   url,
   params=query
)

   print(response.text)



