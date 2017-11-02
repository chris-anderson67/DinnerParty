from flask import Flask
from config import firebase_path
app = Flask(__name__)

@app.route("/")
def index():
    return "Hello World!"

if __name__ == '__main__':
    print firebase_path
    app.run()
