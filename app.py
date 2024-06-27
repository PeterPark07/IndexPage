from flask import Flask, render_template, request, redirect, url_for, jsonify, session
from database import mongo_client
from bson import ObjectId

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # For session management

def fetch_collections_map():
    db_collections_map = {}
    system_dbs = {'admin', 'local', 'config'}  # System databases to exclude
    database_names = [db for db in client.list_database_names() if db not in system_dbs]
    for db_name in database_names:
        db = mongo_client[db_name]
        db_collections_map[db_name] = db.list_collection_names()
    return db_collections_map

# Fetch collections map initially
db_collections_map = fetch_collections_map()


# Default database and collection
default_db = 'chat'
default_collection = 'log'

@app.route('/', methods=['GET', 'POST'])
def home():
    if 'selected_db_collection' not in session:
        session['selected_db_collection'] = f"{default_db}/{default_collection}"  # Default db/collection if not set

    selected_db, selected_collection = session['selected_db_collection'].split('/')
    collections_list = db_collections_map.get(selected_db, [])

    if request.method == 'POST':
        selected_db_collection = request.form.get('db_collection', f"{default_db}/{default_collection}")

        # Validate and split the selected_db_collection
        selected_db, selected_collection = selected_db_collection.split('/')
        if selected_db in db_collections_map and selected_collection in db_collections_map[selected_db]:
            session['selected_db_collection'] = selected_db_collection
        else:
            return render_template('entries.html', db_collections_map=db_collections_map,
                                   error_message=f'Invalid selection: "{selected_db_collection}"')

    db_name = selected_db
    collection_name = selected_collection
    db = mongo_client[db_name]
    entries_data = list(db[collection_name].find())  # Limiting the number of entries for display

    return render_template('entries.html', db_collections_map=db_collections_map,
                           selected_db=db_name, selected_collection=collection_name, entries=entries_data)


@app.route('/delete_entry/<string:entry_id>', methods=['DELETE'])
def delete_entry(entry_id):
    entry_object_id = ObjectId(entry_id)
    selected_collection = session.get('selected_collection', 'log')
    db[selected_collection].delete_one({'_id': entry_object_id})
    return jsonify({'success': True})

if __name__ == '__main__':
    app.run(debug=True)
