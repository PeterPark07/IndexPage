from flask import Flask, render_template, request
from database import db

app = Flask(__name__)

# Mock MongoDB data for demonstration
default_collection = "log"  # Set a default collection
collections_list = ["log", "messages", "torrentlog"]
mongo_data = db[default_collection].find()  # Fetch data from the default collection

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        selected_collection = request.form.get('collection_name', default_collection)

        # Check if the selected collection exists in the database
        if selected_collection not in db.list_collection_names():
            return render_template('home.html', collections_list=collections_list, error_message=f'Collection "{selected_collection}" not found.')

        # Retrieve data from the selected collection
        collection = db[selected_collection]
        entries_data = collection.find()

        return render_template('home.html', collections_list=collections_list, selected_collection=selected_collection, entries=entries_data)

    # On initial GET request, render the home page with the default collection
    return render_template('home.html', collections_list=collections_list, selected_collection=default_collection, entries=mongo_data)

if __name__ == '__main__':
    app.run(debug=True)
