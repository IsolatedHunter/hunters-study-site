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
    if request.args.get('code') != 'utsa2026':
        abort(404)

    portfolio_data = load_json_data('portfolio_data.json')['entries']
    academics_data = load_json_data('academics.json')
    
    # Handle both list and dict structures for academics
    classes = academics_data if isinstance(academics_data, list) else academics_data.get("classes", [])

    expertise = ["Mathematical Physics", "Numerical Integration", "Python (NumPy/Matplotlib)", "Community Leadership", "Data Visualization"]

    return render_template('master_dossier.html', 
                           entries=portfolio_data, 
                           classes=classes,
                           expertise=expertise)

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

# --- Error Handlers ---

@app.errorhandler(404)
def page_not_found(e):
    # This triggers if a URL doesn't exist
    return render_template('error.html', 
        error_code=404, 
        error_message="The page you're looking for has vanished into a black hole.",
        traceback="N/A - Page simply not found."
    ), 404

@app.errorhandler(403)
def forbidden(e):
    # This triggers if the Dossier Code is wrong
    return render_template('error.html', 
        error_code=403, 
        error_message="Access Denied. A valid credentials code is required to view this dossier.",
        traceback="Security Exception: Unauthorized Access Attempt"
    ), 403

@app.errorhandler(500)
def internal_error(e):
    # This triggers if your Python code crashes
    # It captures the "traceback" so you can fix the bug
    tb = traceback.format_exc() 
    return render_template('error.html', 
        error_code=500, 
        error_message="Our server encountered a glitch in the simulation.",
        traceback=tb
    ), 500

if __name__ == '__main__':
    app.run(debug=True)