from flask import Flask, request
from flask_restful import Api, Resource, reqparse
import werkzeug
import numpy as np
import cv2
import scipy
import scipy.stats

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

        cv2.imwrite('test.png', img)

        return {"mask": img.tolist()}


api.add_resource(ImageProcess, "/")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5001", debug=True)
