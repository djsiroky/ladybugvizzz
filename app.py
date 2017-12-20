from flask import Flask, request, jsonify
from flask_cors import CORS
from returnTemperatureData import lambda_handler

app = Flask(__name__)
CORS(app)

@app.route("/temps")
def hello():
    loc = request.args.get('loc')
    print(loc)
    res = lambda_handler(loc)

    return jsonify(res)