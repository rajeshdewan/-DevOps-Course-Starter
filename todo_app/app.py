from flask import Flask,request,render_template,redirect,url_for,flash
from todo_app.data.session_items import get_items,add_item,get_item,save_item,delete_item
from operator import itemgetter
from todo_app.flask_config import Config

app = Flask(__name__)
app.config.from_object(Config)



# Call to add an item or display the page
@app.route('/', methods=['GET', 'POST'])
def index():
    listofitems = get_items()
    

    sortedListofitems = sorted(listofitems, key=itemgetter('status') )

    
    if request.method == 'POST':
        title = request.form.get('itemname')
        add_item(title)
        ##return  render_template('index.html',getlist = listofitems)
        return redirect(url_for('index'))
          
    return render_template('index.html',getlist = sortedListofitems)

#Call to mark the item complete
@app.route('/complete' ,methods=['POST'])
def mark_complete():
    itemid = request.form.get('itemcomplete')
    item =get_item(itemid)
    item["status"] = "Complete"
    save_item(item)
    return redirect(url_for('index'))


# Call to delete function
@app.route('/delete', methods=['POST'])
def remove_item():
    
    itemid = request.form.get('itemdelete')
    itemidnum = int(itemid)
    
    delete_item(itemidnum)
    
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run()


#This is to call the application 
#http://127.0.0.1:5000/