# app.py

from flask import Flask, render_template, request, redirect, url_for, jsonify
from database import db
from bson import ObjectId


import socket

# Get the hostname of the server
hostname = socket.gethostname()

# Get the IP address of the server
ip_address = socket.gethostbyname(hostname)

print(f"Server IP Address: {ip_address}")


app = Flask(__name__)

# Mock MongoDB data for demonstration
default_collection = "log"  # Set a default collection
collections_list = ["log", "messages", "torrentlog"]
mongo_data = db[default_collection].find()  # Fetch data from the default collection

selected_collection = default_collection  # Initialize selected_collection with default value

@app.route('/', methods=['GET', 'POST'])
def home():
    global selected_collection  # Use the global keyword to modify the global variable

    if request.method == 'POST':
        selected_collection = request.form.get('collection_name', default_collection)

        # Check if the selected collection exists in the database
        if selected_collection not in db.list_collection_names():
            return render_template('entries.html', collections_list=collections_list, error_message=f'Collection "{selected_collection}" not found.', entries=mongo_data)

        # Retrieve data from the selected collection
        collection = db[selected_collection]
        entries_data = collection.find()

        return render_template('entries.html', collections_list=collections_list, selected_collection=selected_collection, entries=entries_data)

    # On initial GET request, render the home page with the default collection
    return render_template('entries.html', collections_list=collections_list, selected_collection=selected_collection, entries=mongo_data)

@app.route('/delete_entry/<string:entry_id>', methods=['POST'])
def delete_entry(entry_id):
    # Convert the entry_id to ObjectId
    entry_object_id = ObjectId(entry_id)

    # Delete the entry with the given _id from the collection
    db[selected_collection].delete_one({'_id': entry_object_id})

    # Retrieve data from the selected collection
    collection = db[selected_collection]
    entries_data = collection.find()

    # Render the home page with the selected collection and updated entries
    return render_template('entries.html', collections_list=collections_list, selected_collection=selected_collection, entries=entries_data)

if __name__ == '__main__':
    app.run(debug=True)
