import json
import os
import traceback
from flask import Flask, render_template, abort

app = Flask(__name__)
app.secret_key = os.urandom(24)
app.url_map.strict_slashes = False

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, 'data')

def load_json_data(filename):
    file_path = os.path.join(BASE_DIR, filename)
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Database file '{filename}' is missing at {file_path}")
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/quiz/<course_num>/<week>')
def quiz_page(course_num, week):
    # This route serves the universal quiz.html template
    # The frontend JS will fetch the JSON based on these parameters
    return render_template('quiz.html', course_num=course_num, week=week)

@app.route('/api/quiz/<course_num>/<week>')
def get_quiz_data(course_num, week):
    try:
        quiz_file = os.path.join(BASE_DIR, 'static', 'courses', course_num, f'{week}.json')
        if not os.path.exists(quiz_file):
            abort(404)
        with open(quiz_file, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        print(f"Error loading quiz: {e}")
        abort(500)

@app.route('/chem/study-sheets')
def chem_study_sheets():
    try:
        data = load_json_data('chem_study_sheets.json')
        return render_template('chem_study_sheets.html', sheets=data.get('sheets', []), title="Chemistry Study Sheets")
    except FileNotFoundError:
        return render_template('chem_study_sheets.html', sheets=[], title="Chemistry Study Sheets")
    except Exception as e:
        print(f"Error loading chemistry study sheets: {e}")
        abort(500)

@app.route('/course/<course_num>')
def course_page(course_num):
    try:
        data = load_json_data(f'{course_num}_materials.json')
        course_info = data.get('course_info', {})
        quizzes = data.get('quizzes', [])
        return render_template('course.html', course_num=course_num, course_info=course_info, materials=quizzes, title=course_info.get('name', 'Course'))
    except FileNotFoundError:
        return render_template('course.html', course_num=course_num, course_info={}, materials=[], title='Course')
    except Exception as e:
        print(f"Error loading course materials: {e}")
        abort(500)

@app.errorhandler(Exception)
def handle_error(e):
    error_code = getattr(e, 'code', 500)
    error_messages = {404: "Page vanished into a black hole.", 500: "Glitch in the simulation."}
    return render_template('error.html', 
        error_code=error_code, 
        error_message=error_messages.get(error_code, "Error"),
        traceback=traceback.format_exc() if error_code == 500 else "N/A"
    ), error_code

if __name__ == '__main__':
    app.run(debug=True)