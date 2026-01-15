import json
import os
import traceback
from flask import Flask, render_template, abort, request

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def load_json_data(filename):
    file_path = os.path.join(BASE_DIR, filename)
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Database file '{filename}' is missing at {file_path}")
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)

@app.route('/')
def home():
    return render_template('index.html', title="Home")

@app.route('/master-dossier')
def master_dossier():
    # The 'password' is checked in the URL: /master-dossier?code=utsa2026
    if request.args.get('code') != 'utsa2026':
        abort(404)
    portfolio_data = load_json_data('portfolio_data.json')['entries']
    academics_data = load_json_data('academics.json')
    # If academics is a list, use it; otherwise get "classes"
    classes = academics_data if isinstance(academics_data, list) else academics_data.get("classes", [])

    return render_template('master_dossier.html', 
                           entries=portfolio_data, 
                           classes=classes)

@app.route('/portfolio')
def portfolio():
    # Load your new JSON structure
    data = load_json_data('portfolio_data.json')
    # Pass the list of entries
    return render_template('portfolio.html', entries=data['entries'])

@app.route('/portfolio/<int:entry_id>')
def portfolio_detail(entry_id):
    data = load_json_data('portfolio_data.json')
    # Access by list index
    entry = data['entries'][entry_id]
    return render_template('portfolio_detail.html', project=entry)

@app.route('/academics')
def academics():
    try:
        data = load_json_data('academics.json')
        # Ensure we are passing a list to the template
        course_list = data if isinstance(data, list) else data.get("classes", [])
        return render_template('academics.html', classes=course_list, title="Academics")
    except Exception as e:
        print(f"Error loading academics: {e}")
        abort(500)

@app.route('/linktree')
def linktree():
    return render_template('linktree.html', title="Links")

# --- Error Handlers ---

@app.errorhandler(404)
def page_not_found(e):
    return render_template('error.html', error_code=404, error_message="Page not found."), 404

@app.errorhandler(Exception)
def handle_unexpected_error(e):
    tb = traceback.format_exc()
    print(tb) 
    return render_template(
        'error.html', 
        error_code=500, 
        error_message=str(e), 
        traceback=tb
    ), 500

if __name__ == '__main__':
    app.run(debug=True)