from flask import Flask, render_template, request, url_for, redirect
from pymongo import MongoClient
import certifi
from bson.objectid import ObjectId

# ---------------------------
# Setup
app = Flask(__name__)

ca = certifi.where()
uri = "mongodb+srv://el634dev:ZhjvzSZH5otHvfRq@cluster0.ummojnh.mongodb.net/?retryWrites=true&w=majority"

# Create a new client and connect to the server
client = MongoClient(uri, tlsCAFile=ca)
# Grab the database and the collection
db = client.todo_list
todos = db.todos

# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)
 
# -------------------
# Routes

# Home Page
@app.route('/', methods=('GET', 'POST'))
def index():
    """Handle POST request and show home page"""
    if request.method=='POST':
        content = request.form['content']
        priority = request.form['priority']
        todos.insert_one({'content': content, 'priority': priority})
        return redirect(url_for('index'))

    all_todos = todos.find().collation({'locale': 'en'}).sort('content')
    return render_template('index.html', todos=all_todos)

# --------------------------
# Delete
@app.post('/<id>/delete/')
def delete(id):
    """Delete todo item"""
    todos.delete_one({"_id": ObjectId(id)})
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=False)
