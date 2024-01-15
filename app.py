from flask import Flask, request, jsonify
import json, numpy as np, cv2

app = Flask(__name__)

@app.route("/", methods=["GET"])
def index():
    return "Accessed to index."

@app.route("/shape", methods=["GET"])
def shape():
    return "Accessed to shape recognizer."

@app.route("/shape", methods=["POST"])
def recognize_shapes_by_coordinates():
    data = json.loads(request.data)
    coords = data["coords"]
    
    x_list_raw = [[p[0] for p in l] for l in coords]
    y_list_raw = [[p[1] for p in l] for l in coords]
    x_list = []
    y_list = []
    for a in x_list_raw: x_list += a
    for b in y_list_raw: y_list += b
    max_x = max(x_list)
    max_y = max(y_list)
    min_x = min(x_list)
    min_y = min(y_list)
    
    zeros = np.zeros((int(max_y-min_y+200), int(max_x-min_x+200), 3), np.uint8)
    scene = np.where(zeros == 0, 255, zeros)
    for line in coords:
        for i in range(1, len(line)):
            p1 = (int(line[i-1][0]-min_x+100), int(line[i-1][1]-min_y+100))
            p2 = (int(line[i][0]-min_x+100), int(line[i][1]-min_y+100))
            scene = cv2.line(scene, p1, p2, [0, 0, 0], 2)
    scene = cv2.flip(scene, 0)
    
    th, scene = cv2.threshold(scene, 200, 255, cv2.THRESH_BINARY_INV)
    h, w = scene.shape[:2]
    mask = np.zeros((h+2, w+2), np.uint8)
    cv2.floodFill(scene, mask, (0, 0), (255, 255, 255))
    
    gray = cv2.cvtColor(scene, cv2.COLOR_BGR2GRAY)
    _, threshold = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY) 
    blurred = cv2.blur(threshold, (20, 20))
    contours, _ = cv2.findContours(blurred, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE) 
      
    i = 0
    out = []
    for contour in contours: 
        if i == 0: 
            i = 1
            continue
      
        approx = cv2.approxPolyDP(contour, 0.01 * cv2.arcLength(contour, True), True) 
        cv2.drawContours(scene, [contour], 0, (0, 0, 255), 3) 
      
        M = cv2.moments(contour) 
        if M["m00"] != 0.0: 
            x = int(M["m10"]/M["m00"]) 
            y = int(M["m01"]/M["m00"]) 
        
        if len(approx) < 10: out.append(len(approx))
        else: out.append("inf")
    
    return jsonify(max(set(out), key=out.count))

if __name__ == "__main__":
    app.run_server(debug=False, port=8547)
