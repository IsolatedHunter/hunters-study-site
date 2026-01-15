import json
from flask import Flask, render_template, url_for, abort

app = Flask(__name__)

# Helper function to read your laptop-managed database
def get_site_data():
    try:
        with open('data.json', 'r') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        # Returns empty structure if file is missing or broken
        return {"projects": {}, "classes": []}

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/projects', strict_slashes=False)
def projects():
    data = get_site_data()
    # Pulls ONLY the projects section for the grid
    return render_template('projects.html', projects=data.get("projects", {}))

@app.route('/projects/<project_id>', strict_slashes=False)
def project_detail(project_id):
    data = get_site_data()
    # Looks for specific project within the projects dictionary
    project = data.get("projects", {}).get(project_id)
    
    if not project:
        abort(404)
        
    return render_template('project_detail.html', project=project)

@app.route('/academics', strict_slashes=False)
def academics():
    data = get_site_data()
    # Pulls ONLY the classes list for the transcript page
    return render_template('academics.html', classes=data.get("classes", []))

@app.route('/linktree', strict_slashes=False)
def linktree():
    return render_template('linktree.html')

@app.errorhandler(404)
def page_not_found(e):
    return render_template('error.html', 
                           error_code=404, 
                           error_message="We couldn't find the page you were looking for."), 404

@app.errorhandler(500)
def server_error(e):
    return render_template('error.html', 
                           error_code=500, 
                           error_message="Our server is having a moment. Please try again later."), 500

if __name__ == '__main__':
    app.run(debug=True)