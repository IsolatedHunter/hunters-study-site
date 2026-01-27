
import json
import os
import traceback
import secrets
from flask import Flask, render_template, abort, request, flash


app = Flask(__name__)
if 'SECRET_KEY' in os.environ:
    app.secret_key = os.environ['SECRET_KEY']
else:
    app.secret_key = secrets.token_urlsafe(32)
    print("[WARNING] No SECRET_KEY set in environment. Generated a random secret key for this session.")

# Allow routes to be accessed with or without trailing slashes
app.url_map.strict_slashes = False

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def load_json_data(filename):
    file_path = os.path.join(BASE_DIR, filename)
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Database file '{filename}' is missing at {file_path}")
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def title_to_slug(title):
    """Convert title to URL-friendly slug"""
    return title.lower().strip().replace(' ', '-').replace('&', 'and')

@app.route('/')
def home():
    return render_template('index.html', title="Home")

@app.route('/portfolio')
def portfolio():
    # Load your new JSON structure
    data = load_json_data('portfolio_data.json')
    # Pass the list of entries
    return render_template('portfolio.html', entries=data['entries'])

@app.route('/portfolio/<slug>')
def portfolio_detail(slug):
    data = load_json_data('portfolio_data.json')
    # Find entry by matching slug to title
    for entry in data['entries']:
        if title_to_slug(entry['title']) == slug:
            return render_template('portfolio_detail.html', project=entry)
    abort(404)

@app.route('/campaign')
def campaign():
    return render_template('campaign.html')

@app.route('/campaign/join', methods=['GET', 'POST'])
def join_campaign():
    if request.method == 'POST':
        # Here you would normally save to a database or send an email
        name = request.form.get('name')
        email = request.form.get('email')
        role = request.form.get('role')
        flash("Thanks for joining the team, Hunter will reach out soon!")
    return render_template('join.html')

@app.route('/resume')
def resume():
    return render_template('resume.html')

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

@app.route('/editor')
def editor():
    return render_template('description_editor.html')

# --- Error Handlers ---

@app.errorhandler(Exception)
def handle_error(e):
    error_code = getattr(e, 'code', 500)
    
    error_messages = {
        404: "The page you're looking for has vanished into a black hole.",
        500: "Our server encountered a glitch in the simulation."
    }
    
    error_message = error_messages.get(error_code, f"Error {error_code} occurred.")
    
    tb = traceback.format_exc() if error_code == 500 else "N/A"
    
    return render_template('error.html', 
        error_code=error_code, 
        error_message=error_message,
        traceback=tb
    ), error_code

if __name__ == '__main__':
    app.run(debug=True)