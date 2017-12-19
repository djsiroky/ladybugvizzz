from flask import Flask, request
from flask_cors import CORS
from returnTemperatureData import lambda_handler

app = Flask(__name__)
CORS(app)

@app.route("/temps")
def hello():
    loc = request.args.get('loc')
    res = lambda_handler(loc)

    return res