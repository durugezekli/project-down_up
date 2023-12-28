from flask import Flask, request, jsonify
import json

app = Flask(__name__)

@app.route("/", methods=["GET"])
def index():
    return "Accessed"

@app.route("/", methods=['POST'])
def recognize_shapes_by_lines():
    data = json.loads(request.data)
    return type(data["coords"]) + " -> " + str(data)[:50] 

if __name__ == "__main__":
    app.run_server(debug=False, port=8547)

# import cv2
# import numpy as np

# coords = [[[574.1757978796959, 1649.7025019675493], [512.7970393002033, 1539.3802091479301], [444.2480427622795, 1415.689273327589], [396.49456280469894, 1303.5847313702106], [358.8270979523659, 1186.779966801405], [318.81650257110596, 1080.104253590107]], [[212.5152761042118, 1083.571270108223], [315.7804915010929, 1078.228983283043], [418.92537650465965, 1077.6112732291222], [546.8571970462799, 1089.9338269233704], [663.4208181500435, 1105.265421718359], [763.7697418928146, 1108.5176788270473]], [[773.687255859375, 1025.4837337136269], [737.6328356862068, 1124.194464534521], [698.2387486696243, 1245.5570384860039], [648.7122122645378, 1357.379293590784], [605.7194682955742, 1463.3325868844986], [568.7486463189125, 1556.341513991356], [532.1370790600777, 1661.9638772308826]]]

# x_list_raw = [[p[0] for p in l] for l in coords]
# y_list_raw = [[p[1] for p in l] for l in coords]
# x_list = []
# y_list = []
# for a in x_list_raw: x_list += a
# for b in y_list_raw: y_list += b
# max_x = max(x_list)
# max_y = max(y_list)
# min_x = min(x_list)
# min_y = min(y_list)

# zeros = np.zeros((int(max_y-min_y+200), int(max_x-min_x+200), 3), np.uint8)
# scene = np.where(zeros == 0, 255, zeros)
# for line in coords:
#     for i in range(1, len(line)):
#         p1 = (int(line[i-1][0]-min_x+100), int(line[i-1][1]-min_y+100))
#         p2 = (int(line[i][0]-min_x+100), int(line[i][1]-min_y+100))
#         scene = cv2.line(scene, p1, p2, [0, 0, 0], 2)
# scene = cv2.flip(scene, 0)

# th, scene = cv2.threshold(scene, 200, 255, cv2.THRESH_BINARY_INV)
# h, w = scene.shape[:2]
# mask = np.zeros((h+2, w+2), np.uint8)
# cv2.floodFill(scene, mask, (0, 0), (255, 255, 255))

# gray = cv2.cvtColor(scene, cv2.COLOR_BGR2GRAY)
# _, threshold = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY) 
# contours, _ = cv2.findContours(threshold, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE) 
  
# i = 0
# for contour in contours: 
#     if i == 0: 
#         i = 1
#         continue
  
#     approx = cv2.approxPolyDP(contour, 0.01 * cv2.arcLength(contour, True), True) 
#     cv2.drawContours(scene, [contour], 0, (0, 0, 255), 3) 
  
#     M = cv2.moments(contour) 
#     if M["m00"] != 0.0: 
#         x = int(M["m10"]/M["m00"]) 
#         y = int(M["m01"]/M["m00"]) 
  
#     out = []
#     if len(approx) < 6: out.append(len(approx))
#     else: out.append(-1)
