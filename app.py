from flask import Flask, request, jsonify
import json, numpy as np, random as rd

app = Flask(__name__)

@app.route("/", methods=["GET"])
def index():
    return "Accessed to index."

# LETTER
@app.route("/letter", methods=["GET"])
def letter():
    return "Accessed to letter audio recognizer."

@app.route("/letter", methods=["POST"])
def recognize_letters_by_audio():
    data = json.loads(request.data)

    return jsonify(rd.choice([True, False]))

# LETTER SEQUENCE
@app.route("/letter-sequence", methods=["GET"])
def letter_sequence():
    return "Accessed to letter sequence audio recognizer."

@app.route("/letter-sequence", methods=["POST"])
def recognize_letter_sequences_by_audio():
    data = json.loads(request.data)

    return jsonify(rd.choice([True, False]))

# SHAPE
@app.route("/shape", methods=["GET"])
def shape():
    return "Accessed to shape audio recognizer."

@app.route("/shape", methods=["POST"])
def recognize_shapes_by_audio():
    data = json.loads(request.data)

    return jsonify(rd.choice([True, False]))

# NUMBER
@app.route("/number", methods=["GET"])
def number():
    return "Accessed to number audio recognizer."

@app.route("/number", methods=["POST"])
def recognize_numbers_by_audio():
    data = json.loads(request.data)

    return jsonify(rd.choice([True, False]))

if __name__ == "__main__":
    app.run_server(debug=False, port=8547)
