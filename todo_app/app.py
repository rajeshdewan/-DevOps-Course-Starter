from flask import Flask,request,render_template,redirect,url_for
from todo_app.flask_config import Config
from todo_app.data.session_items import  markcomplete,putToDoItems,getallitems,ViewModel,getonlytodoitems

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config())

    # Call to display the page
    @app.route('/', methods=['GET'])
    def index():
        listofitems = getallitems() ## Get a list of all items (to do and done)
        #listofitems = getonlytodoitems() ##Get a list of all items (to do only)
        sortedListofitems = sorted(listofitems, key=lambda item: item.status,reverse=True )
            
        item_view_model = ViewModel(sortedListofitems)
        return render_template('index.html',view_model=item_view_model)
        
        # return render_template('index.html',getlist = sortedListofitems)

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

    return app

