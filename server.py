from flask import Flask

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