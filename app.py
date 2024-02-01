from flask import Flask, render_template
import os

app = Flask(__name__)
mongo = os.getenv('api')

# Mock MongoDB data for demonstration
mongo_data = [{"id": 1, "name": "Entry 1"}, {"id": 2, "name": "Entry 2"}]

@app.route('/')
def entries():
    return render_template('entries.html', entries=mongo_data)

if __name__ == '__main__':
    app.run(debug=True)
