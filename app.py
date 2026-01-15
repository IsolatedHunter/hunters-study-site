import json
import os
import traceback
from flask import Flask, render_template, abort

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

@app.route('/projects', strict_slashes=False)
def projects():
    # Load from projects.json
    data = load_json_data('projects.json')
    all_projects = data.get("projects", {})
    return render_template('projects.html', projects=all_projects, title="Projects")

@app.route('/projects/<project_id>', strict_slashes=False)
def project_detail(project_id):
    data = load_json_data('projects.json')
    project = data.get("projects", {}).get(project_id)
    if not project:
        abort(404)
    return render_template('project_detail.html', project=project, title=project.get('title'))

@app.route('/academics')
def academics():
    # Load from academics.json
    # If academics.json is just a list [{}, {}], 'data' will be that list
    data = load_json_data('academics.json')
    
    # Logic check: if your JSON is a list, pass it directly. 
    # If it's a dict like {"classes": []}, use data.get("classes")
    if isinstance(data, list):
        course_list = data
    else:
        course_list = data.get("classes", [])
        
    return render_template('academics.html', classes=course_list, title="Academics")

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