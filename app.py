from flask import Flask, request, jsonify

app = Flask(__name__)

# https://algo-ui.vercel.app/apis/response?status=success&request_token=ZtoCMi8wWy9WsRP3mIXfKoGbdYG446ZB&action=login


#access_token endpoint(params: request_token)
@app.route('/response', methods=['GET'])
def param():
    if request.method == 'GET':
        if request.args:
            if request.args.get('request_token', default=None, type=str) is not None and len(request.args['request_token']) != 0:
                token = request.args['request_token']
                print(token)
                return 'Your access token is: {}'.format(token),201
            else:
                return "Access token must not be empty",202
        else:
            return 'Access token not found',203
    else:
        return 'Mthod not allowed',405



if __name__ == '__main__':
    app.run(debug=True)