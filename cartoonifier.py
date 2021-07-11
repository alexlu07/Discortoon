import cv2
import numpy as np
import os
import requests

class Cartoonifier:

    def __init__(self):
        with open("credentials.txt", "r") as f:
            _ = f.readline()
            _ = f.readline()
            _ = f.readline()
            self.imageshack_key = f.readline().strip()

        self.image_dir = "./cartoonify"
        self.input_name = "input"
        self.output_file = "output.png"

        self.line_size = 7
        self.blur_value = 7
        self.total_color = 9

    def read_file(self):
        # for f in os.listdir(self.image_dir):
        #     split = os.path.splitext(f)
        #     if split[0] == self.input_name:
        #         self.ext = split[1]

        img = cv2.imread(self.image_dir + "/" + self.input_name + ".png")
        # print(image)
        # img = cv2.imread(image)
        return img

    def edge_mask(self, img, line_size, blur_value):
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        gray_blur = cv2.medianBlur(gray, blur_value)
        edges = cv2.adaptiveThreshold(gray_blur, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, line_size, blur_value)

    def color_quantization(self, img, k):
        data = np.float32(img).reshape((-1, 3))

        criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 20, 0.001)

        ret, label, center = cv2.kmeans(data, k, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)
        center = np.uint8(center)
        result = center[label.flatten()]
        result = result.reshape(img.shape)
        return result

    def write_file(self, img):
        # cv2.imwrite(self.image_dir + "/" + self.output_file, img)

        data = {"key": self.imageshack_key,
                    "format": "json"}

        # print(cv2.imencode(".png", img))
        response = requests.post("https://post.imageshack.us/upload_api.php", data=data, files={"fileupload": cv2.imencode(".png", img)[1].tobytes()})
        try:
            return response.json()["links"]["image_link"]
        except Exception as e:
            print(e)
            return False

    def cartoonify(self):
        img = self.read_file()

        edges = self.edge_mask(img, self.line_size, self.blur_value)
        img = self.color_quantization(img, self.total_color)
        blurred = cv2.bilateralFilter(img, d=7, sigmaColor=200,sigmaSpace=200)

        cartoon = cv2.bitwise_and(blurred, blurred, mask=edges)
        return self.write_file(cartoon)
