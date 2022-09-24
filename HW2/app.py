from flask import Flask, make_response, request, json
from werkzeug.exceptions import HTTPException

app = Flask(__name__)

storage = dict()

def generateHello():
    return 'HSE One Love!'

@app.errorhandler(HTTPException)
def handle_exception(e):
    response = make_response()
    response.status_code = 405
    return response

@app.get('/hello')
def hello():
    response = make_response(generateHello(), 200)
    response.content_type = 'text/plain'
    return response

@app.get('/get/<key>')
def get_key(key):
    response = make_response()
    if key not in storage:
        response.status_code = 404
    else:
        response = app.response_class(
            response = json.dumps({
                'key': key,
                'value': storage[key]
            }),
            status = 200,
            content_type = 'application/json'
        )

    return response

@app.post('/set')
def set_key():
    response = make_response()
    if request.content_type == 'application/json':
        content = request.get_json()
        if 'key' not in content or 'value' not in content:
            response.status_code = 400
        else:
            storage[content['key']] = content['value']
            response.status_code = 200
    else:
        response.status_code = 415
    return response
    
@app.post('/devide')
def devide():
    response = make_response()
    response.content_type = 'text/plain'
    if request.content_type == 'application/json':
        content = request.get_json()
        if 'dividend' not in content or 'divider' not in content:
            response.status_code = 400
        else:
            dividend = content['dividend']
            divider = content['divider']
            if divider == 0:
                response.status_code = 400
            else:
                response.set_data(str(dividend / divider))
                response.status_code = 200
    else:
        response.status_code = 415

    return response

if __name__ == '__main__':
    app.run()