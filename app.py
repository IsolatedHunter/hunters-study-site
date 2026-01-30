import json
import os
import traceback
import smtplib
from email.message import EmailMessage
from dotenv import load_dotenv # type: ignore
from flask import Flask, render_template, abort, request, flash, redirect, url_for

load_dotenv()
app = Flask(__name__)
app.secret_key = os.urandom(24)

# Allow routes to be accessed with or without trailing slashes
app.url_map.strict_slashes = False

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

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