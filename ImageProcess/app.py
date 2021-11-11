from flask import Flask, request
from flask_restful import Api, Resource, reqparse
import werkzeug
import numpy as np
import cv2
import scipy
import scipy.stats
import logging

app = Flask(__name__)
api = Api(app)


class ImageProcess(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument(
            "data",
            type=werkzeug.datastructures.FileStorage,
            location="files",
            required=True,
            help="You must provide image data to process!",
        )

        args = parser.parse_args()

        try:
            file = args["data"]
            npimg = np.fromfile(file, np.uint8)
            img = cv2.imdecode(npimg, cv2.IMREAD_GRAYSCALE)
        except:
            return {"error": "Image could not be decoded"}, 400
        
        if img is None:
            return {"error": "Image could not be decoded"}, 400

        blur = cv2.GaussianBlur(img, (3, 3), 0)
        res, thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_OTSU)

        # which is greater?
        # if scipy.stats.mode(thresh) == True:
        #     thresh = not thresh

        img = np.zeros((thresh.shape[0], thresh.shape[1], 3))

        cv2.imwrite('test.png', img)

        img[:,:,0] = thresh[:,:]
        img[:,:,1] = thresh[:,:]
        img[:,:,2] = thresh[:,:]

        count_true = 0
        total_count = 0
        for row in img:
            for cell in row:
                total_count += 1
                if cell[0] == 255:
                    count_true += 1

        if count_true < total_count / 2:
            for row in range(img.shape[0]):
                for cell in range(img.shape[1]):
                    if img[row][cell][0] == 255:
                        img[row][cell][:] = 0
                    else:
                        img[row][cell][:] = 255

        cv2.imwrite('test.png', img)

        return {"mask": img.tolist()}


api.add_resource(ImageProcess, "/")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5001", debug=True)
else:
    gunicorn_logger = logging.getLogger('gunicorn.error')
    app.logger.handlers = gunicorn_logger.handlers
    app.logger.setLevel(gunicorn_logger.level)