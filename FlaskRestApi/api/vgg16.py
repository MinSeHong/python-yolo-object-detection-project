'''
python -m pip install --upgrade pip
pip install tensorflow
pip install pillow
pip install opencv-python

아래 에러가 났을때 해결책
AttributeError: module 'tensorflow._api.v2.compat.v2.internal' has no attribute 'register_load_context_function'
TensorFlow 버전 2.11 이상에서 발생하며, Keras를 사용하여 모델을 학습하거나 평가할 때 발생
TensorFlow 2.11에서 register_load_context_function이라는 함수가 제거되었기 때문에 이 에러가 발생
1. TensorFlow 버전을 2.10 이하로 다운그레이드
pip install tensorflow==2.10
2. Keras 버전을 2.7.0 이하로 다운그레이드
pip install keras==2.7.0
3. TensorFlow nightly 버전 사용
TensorFlow nightly 버전에는 register_load_context_function 함수가 포함
pip install tf-nightly
'''
from flask_restful import Resource
from flask import request,make_response
from tensorflow import keras
from tensorflow.keras.applications.imagenet_utils import decode_predictions
from tensorflow.keras.preprocessing import image #이미지 전처리용
from tensorflow.keras.applications.vgg16 import preprocess_input
import base64
from PIL import Image

import json
import numpy as np
import io

class VGG16CNN(Resource):
    def __init__(self):
        #모델 로드(#파일은 프로젝트 루트에)
        self.model_vgg16 = keras.models.load_model('vgg16_model.h5')
    def post(self):
        base64Encoded = request.form['base64Encoded']
        # base64 이미지 인코딩 문자열을 decode
        image_b64 = base64.b64decode(base64Encoded)
        image_memory = Image.open(io.BytesIO(image_b64))#이미지 파일로 디코딩

        image_memory = np.asarray(image_memory.resize((224, 224)))
        dog_image_array = image.img_to_array(image_memory)
        dog_image_array_input = np.expand_dims(dog_image_array, axis=0)
        dog_image_array_output = preprocess_input(dog_image_array_input)
        y_pred = self.model_vgg16.predict(dog_image_array_output)

        #print(y_pred)
        y_pred_dict={}
        decode_pred = decode_predictions(y_pred, top=5)
        for i, (imagenet_id, label, score) in enumerate(decode_pred[0]):  # imagenet_id는 위 주소에서 확인
            print(f'Top {i + 1}:{imagenet_id}:{label}를 {score * 100}%의 확률로 예측')
            y_pred_dict[f'{i + 1}']=label

        print(y_pred_dict)
        return make_response(json.dumps(y_pred_dict,ensure_ascii=False))
