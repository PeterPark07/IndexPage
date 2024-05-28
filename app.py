from flask import Flask, render_template, request, redirect, url_for, jsonify, session
from database import db
from bson import ObjectId

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # For session management

collections_list = ["log", "messages", "torrentlog", "message_log", "ship"]

@app.route('/', methods=['GET', 'POST'])
def home():
    if 'selected_collection' not in session:
        session['selected_collection'] = 'log'  # Default collection

    selected_collection = session['selected_collection']

    if request.method == 'POST':
        selected_collection = request.form.get('collection_name', 'log')
        if selected_collection in db.list_collection_names():
            session['selected_collection'] = selected_collection
        else:
            return render_template('entries.html', collections_list=collections_list, error_message=f'Collection "{selected_collection}" not found.')

    entries_data = list(db[selected_collection].find().limit(20))  # Limit the number of entries

    return render_template('entries.html', collections_list=collections_list, selected_collection=selected_collection, entries=entries_data)

@app.route('/delete_entry/<string:entry_id>', methods=['DELETE'])
def delete_entry(entry_id):
    entry_object_id = ObjectId(entry_id)
    selected_collection = session.get('selected_collection', 'log')
    db[selected_collection].delete_one({'_id': entry_object_id})
    return jsonify({'success': True})

if __name__ == '__main__':
    app.run(debug=True)
