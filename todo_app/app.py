from flask import Flask,request,render_template,redirect,url_for
from todo_app.flask_config import Config
from todo_app.data.session_items import  markcomplete,putToDoItems,getallitems

app = Flask(__name__)
app.config.from_object(Config)

# Call to display the page
@app.route('/', methods=['GET'])
def index():
    listofitems = getallitems() 
    
    sortedListofitems = sorted(listofitems, key=lambda item: item.status,reverse=True )
          
    return render_template('index.html',getlist = sortedListofitems)

# Call to add an item 
@app.route('/', methods= ['POST'])
def addnewitem():
    newitem = request.form.get('itemname')
    putToDoItems(newitem)
    return redirect(url_for('index'))

#Call to mark the item complete
@app.route('/complete' ,methods=['POST'])
def mark_complete():
    itemid = request.form.get('itemcomplete')
    markcomplete(itemid)
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run()
