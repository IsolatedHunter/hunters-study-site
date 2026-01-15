import json
import os
from flask import Flask, render_template, abort

app = Flask(__name__)

# --- Configuration ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def load_json_file(filename):
    """Safely loads a JSON file from the project directory."""
    file_path = os.path.join(BASE_DIR, filename)
    if not os.path.exists(file_path):
        print(f"WARNING: {filename} not found.")
        return {} if "projects" in filename else []
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"ERROR loading {filename}: {e}")
        return {} if "projects" in filename else []

# --- Routes ---

@app.route('/')
def home():
    return render_template('index.html', title="Home")

@app.route('/projects')
def projects():
    # Load only the projects data
    project_data = load_json_file('projects.json')
    return render_template('projects.html', projects=project_data, title="Projects")

@app.route('/projects/<project_id>')
def project_detail(project_id):
    project_data = load_json_file('projects.json')
    project = project_data.get(project_id)
    if not project:
        abort(404)
    return render_template('project_detail.html', project=project, title=project.get('title'))

@app.route('/academics')
def academics():
    # Load only the academic data
    course_list = load_json_file('academics.json')
    return render_template('academics.html', classes=course_list, title="Academics")

@app.route('/linktree')
def linktree():
    return render_template('linktree.html', title="Links")

@app.errorhandler(404)
def page_not_found(e):
    return render_template('error.html', error_code=404, error_message="Page not found."), 404

if __name__ == '__main__':
    app.run(debug=True)