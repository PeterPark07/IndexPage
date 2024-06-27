from flask import Flask, render_template, request, redirect, url_for, jsonify, session
from database import mongo_client
from bson import ObjectId

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # For session management

db_list = ["chat", "Movie", "Sites"]

# Collections for each database
collections_map = {
    "chat": ["log", "messages", "torrentlog", "message_log", "ship"],
    "Movie": ["movie_info"],
    "Sites": ["cloner", "cloud", "mycloud", "notes", "redirect"]
}

# Default database and collection
default_db = 'chat'
default_collection = 'log'

@app.route('/', methods=['GET', 'POST'])
def home():
    if 'selected_db' not in session:
        session['selected_db'] = default_db  # Set default database if not already set

    selected_db = session['selected_db']
    collections_list = collections_map.get(selected_db, [])

    if 'selected_collection' not in session or session['selected_collection'] not in collections_list:
        session['selected_collection'] = default_collection  # Set default collection if not already set or invalid

    selected_collection = session['selected_collection']

    if request.method == 'POST':
        selected_db = request.form.get('db_name', default_db)
        selected_collection = request.form.get('collection_name', default_collection)

        if selected_db in db_list and selected_collection in collections_map.get(selected_db, []):
            session['selected_db'] = selected_db
            session['selected_collection'] = selected_collection
        else:
            # Handle invalid selections gracefully, perhaps with an error message
            return render_template('entries.html', db_list=db_list, collections_list=collections_map.get(selected_db, []),
                                   error_message=f'Database "{selected_db}" or collection "{selected_collection}" not found.')

    db = mongo_client[session['selected_db']]
    entries_data = list(db[selected_collection].find())  # Limiting the number of entries for display

    return render_template('entries.html', db_list=db_list, collections_list=collections_map.get(selected_db, []),
                           selected_db=selected_db, selected_collection=selected_collection, entries=entries_data)



@app.route('/delete_entry/<string:entry_id>', methods=['DELETE'])
def delete_entry(entry_id):
    entry_object_id = ObjectId(entry_id)
    selected_collection = session.get('selected_collection', 'log')
    db[selected_collection].delete_one({'_id': entry_object_id})
    return jsonify({'success': True})

if __name__ == '__main__':
    app.run(debug=True)
