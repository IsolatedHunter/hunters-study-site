import json
import os
import traceback
from flask import Flask, render_template, abort

app = Flask(__name__)

# Helper to find where your files are located
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def load_json_data(filename):
    """Attempt to load JSON; if it fails, the error will be sent to the error handler."""
    file_path = os.path.join(BASE_DIR, filename)
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)

@app.route('/')
def home():
    return render_template('index.html', title="Home")

@app.route('/projects')
def projects():
    # If projects.json is broken, this will trigger the 500 error page
    data = load_json_data('projects.json')
    return render_template('projects.html', projects=data, title="Projects")

@app.route('/academics')
def academics():
    # If academics.json is broken, this will trigger the 500 error page
    data = load_json_data('academics.json')
    return render_template('academics.html', classes=data, title="Academics")

@app.route('/linktree')
def linktree():
    return render_template('linktree.html', title="Links")

# --- Error Handlers ---

@app.errorhandler(404)
def page_not_found(e):
    return render_template('error.html', error_code=404, error_message="Page not found."), 404

@app.errorhandler(Exception)
def handle_unexpected_error(e):
    # This catches EVERYTHING and sends it to your error.html
    tb = traceback.format_exc()
    return render_template(
        'error.html', 
        error_code=500, 
        error_message=str(e), 
        traceback=tb
    ), 500

if __name__ == '__main__':
    # debug=True is essential to see real errors!
    app.run(debug=True)