from flask import Flask, make_response, request
from werkzeug.exceptions import HTTPException

app = Flask(__name__)

storage = dict()

@app.errorhandler(HTTPException)
def handle_exception(e):
    response = make_response()
    response.status_code = 405
    return response

def generateHello():
    return 'HSE OneLove!'

@app.get('/hello')
def hello():
    response = make_response(generateHello(), 200)
    response.mimetype = 'text/plain'
    return response

@app.get('/get/<key>')
def get_key(key=None):
    response = make_response()
    if storage[key] is None:
        response.status_code = 404
    else:
        response.mimetype = 'application/json'
        response.json = {
            "key": key,
            "value": storage[key]
        }
        response.status_code = 200

    return response

@app.post('/set')
def set_key():
    response = make_response()
    if request.mimetype == 'application/json':
        content = request.get_json()
        if content['key'] is None or content['value'] is None:
            response.status_code = 400
        
        storage[content['key']] = content['value']
        response.status_code = 200
    else:
        response.status_code = 415
    return response
    
@app.post('/devide')
def devide():
    response = make_response()
    response.mimetype = 'text/plain'
    if request.mimetype == 'application/json':
        content = request.get_json()
        if content['dividend'] is None or content['divider'] is None:
            response.status_code = 400
        else:
            dividend = content['dividend']
            divider = content['divider']
            response.set_data(str(dividend / divider))
            response.status_code = 200
    else:
        response.status_code = 415

    return response

if __name__ == '__main__':
    app.run(debug=True)