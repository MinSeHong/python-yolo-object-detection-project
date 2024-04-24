#https://flask.palletsprojects.com/en/3.0.x/deploying/asgi/
#pip install hypercorn #파이썬 기반 ASGI서버(파이썬 3.6이상부터 지원)
#pip install asgiref  #플라스크 앱을 Wsgi로 변환용
#pip install uvicorn  #파이썬 기반 ASGI서버(파이썬 3.7이상부터 지원)
from app import app
from asgiref.wsgi import WsgiToAsgi
import uvicorn

asgi_app = WsgiToAsgi(app)

if __name__ == '__main__':
    uvicorn.run(asgi_app,host='0.0.0.0',port=5000)
