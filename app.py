import json
import os
from flask import Flask, render_template, url_for, abort

app = Flask(__name__)

def get_site_data():
    # Force Python to look in the exact folder where app.py lives
    base_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(base_dir, 'data.json')
    
    if not os.path.exists(file_path):
        print(f"FILE NOT FOUND: {file_path}")
        return {"projects": {}, "classes": []}

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"JSON LOAD ERROR: {e}")
        return {"projects": {}, "classes": []}

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/projects', strict_slashes=False)
def projects():
    data = get_site_data()
    return render_template('projects.html', projects=data.get("projects", {}))

@app.route('/projects/<project_id>', strict_slashes=False)
def project_detail(project_id):
    data = get_site_data()
    project = data.get("projects", {}).get(project_id)
    if not project:
        abort(404)
    return render_template('project_detail.html', project=project)

@app.route('/academics', strict_slashes=False)
def academics():
    try:
        data = get_site_data()
        # Debugging: This will print to your terminal so you can see if data exists
        print(f"DEBUG: Classes found: {len(data.get('classes', []))}")
        
        # Explicitly fetch the list. If it's missing, use an empty list []
        course_list = data.get("classes", [])
        
        return render_template('academics.html', classes=course_list)
    except Exception as e:
        # This logs the EXACT error to your terminal
        print(f"CRITICAL ERROR in /academics: {e}")
        return abort(500)

@app.route('/linktree', strict_slashes=False)
def linktree():
    return render_template('linktree.html')

@app.errorhandler(404)
def page_not_found(e):
    return render_template('error.html', error_code=404, error_message="Page not found."), 404

#@app.errorhandler(500)
#def server_error(e):
#    return render_template('error.html', error_code=500, error_message="Internal server error."), 500

if __name__ == '__main__':
    app.run(debug=True)