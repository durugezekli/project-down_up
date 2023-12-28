from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/", methods=["GET"])
def index():
    return "Accessed"

@app.route("/", methods=['POST'])
def recognize_shapes_by_lines():
    data = json.loads(request.data)
    return str(data)[:10]

if __name__ == "__main__":
    app.run_server(debug=False, port=8547)
