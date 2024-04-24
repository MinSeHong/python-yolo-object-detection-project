'''
https://flask-restful.readthedocs.io/en/latest/
1. pip install flask
2. pip install flask-restful
3. pip install flask_cors
'''
from flask import Flask
from flask_restful import Api
from flask_cors import CORS
import os

from api.vgg16 import VGG16CNN

app = Flask(__name__)
CORS(app)

api = Api(app)

api.add_resource(VGG16CNN,'/vgg16')

from api.mask_detection import MaskDetection
api.add_resource(MaskDetection,'/mask')
if __name__ == '__main__':
    app.run(debug=True)