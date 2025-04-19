from flask import Flask
from flask import make_response

app = Flask(__name__)

@app.route('/')
def home():
    # returning string
    # return "Hello, World!, this is a Flask app running in a virtual environment!"

    # returning json
    return {"message": "Hello, World!, this is a Flask app"}

@app.route('/no_content')
def no_content():
    # returning no content
    return "No content found", 204

@app.route('/exp')
def index_explicit():
    # returning json with make_response() method
    resp = make_response({"message": "Hello, World!, this is a Flask app"})
    resp.status_code = 200
    
    return resp