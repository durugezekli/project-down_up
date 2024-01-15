from flask import Flask, request, jsonify
import json, cv2, numpy as np
from skimage.metrics import structural_similarity as ssim
from os import path

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

    def get_image_by_coords(coords):
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
        zeros = np.zeros((int(max_y-min_y+100), int(max_x-min_x+100), 3), np.uint8)
        scene = np.where(zeros == 0, 255, zeros)
        for line in coords:
            for i in range(1, len(line)):
                p1 = (int(line[i-1][0]-min_x+50), int(line[i-1][1]-min_y+50))
                p2 = (int(line[i][0]-min_x+50), int(line[i][1]-min_y+50))
                scene = cv2.line(scene, p1, p2, [0, 0, 0], 10)
        scene = cv2.resize(scene, (500, 600))
        def pixelate(img, w, h):
            height, width = img.shape[:2]
            temp = cv2.resize(img, (w, h), interpolation=cv2.INTER_LINEAR)
            # res = cv2.resize(temp, (width, height), interpolation=cv2.INTER_NEAREST)
            for y in range(len(temp)):
                for x in range(len(temp[y])):
                    if temp[y][x][0] != 255 or temp[y][x][1] != 255 or temp[y][x][2] != 255:
                        temp[y][x][0], temp[y][x][1], temp[y][x][2] = 0, 0, 0
            # for y in range(len(res)):
            #     for x in range(len(res[y])):
            #         if res[y][x][0] != 255 or res[y][x][1] != 255 or res[y][x][2] != 255:
            #             res[y][x][0], res[y][x][1], res[y][x][2] = 0, 0, 0
            return temp
        return pixelate(scene, 24, 24)
            
    a = cv2.cvtColor(get_image_by_coords(coords), cv2.COLOR_BGR2GRAY) # Test
    
    results = []
    for n in "ABCÇDEFGĞHIJKLMNOÖPRSŞTUÜVYZ":
        print(n) # DEBUG
        
        s = ssim(a, cv2.cvtColor(cv2.imread(path.join("letter_train", f"{n}.jpg")), cv2.COLOR_BGR2GRAY))
        results.append([n, s])
    results = sorted(results, key=lambda x: x[1], reverse=True)[:3]
    
    print(results) # DEBUG
    
    return jsonify(data["answer"] in [x for x, y in results])

if __name__ == "__main__":
    app.run_server(debug=False, port=8547)
