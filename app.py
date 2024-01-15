from flask import Flask, request, jsonify
import json, numpy as np, cv2

app = Flask(__name__)

@app.route("/", methods=["GET"])
def index():
    return "Accessed to index."

@app.route("/letter", methods=["GET"])
def letter():
    return "Accessed to letter recognizer."

@app.route("/letter", methods=["POST"])
def recognize_letters_by_coordinates():
    data = json.loads(request.data)
    coords = data["coords"]

    return jsonify(True)

if __name__ == "__main__":
    app.run_server(debug=False, port=8547)
