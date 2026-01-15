import json
import os
import traceback  # Required to capture the error details
from flask import Flask, render_template, abort

app = Flask(__name__)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def load_json_file(filename):
    file_path = os.path.join(BASE_DIR, filename)
    # If file is missing, we raise an error so the error handler catches it
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"The data file '{filename}' is missing from {BASE_DIR}")
    
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)

@app.route('/')
def home():
    return render_template('index.html', title="Home")

@app.route('/projects')
def projects():
    # If this fails (e.g. bad JSON syntax), it triggers the 500 handler
    project_data = load_json_file('projects.json')
    return render_template('projects.html', projects=project_data, title="Projects")

@app.route('/academics')
def academics():
    course_list = load_json_file('academics.json')
    return render_template('academics.html', classes=course_list, title="Academics")

# --- Enhanced Error Handling ---

@app.errorhandler(404)
def page_not_found(e):
    return render_template('error.html', error_code=404, error_message="Page not found."), 404

@app.errorhandler(500)
@app.errorhandler(Exception) # This catches ALL other Python crashes
def handle_exception(e):
    # Capture the full Python traceback
    tb = traceback.format_exc()
    return render_template(
        'error.html', 
        error_code=500, 
        error_message=str(e),
        traceback=tb # Passing the technical details to the HTML
    ), 500

if __name__ == '__main__':
    app.run(debug=True)