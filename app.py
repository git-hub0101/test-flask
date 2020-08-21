from flask import Flask, request, jsonify, redirect
import psycopg2
import pandas as pd 
import json
from kiteconnect import *
import datetime

app = Flask(__name__)

# https://algo-ui.vercel.app/apis/response?status=success&request_token=ZtoCMi8wWy9WsRP3mIXfKoGbdYG446ZB&action=login
# https://safe-caverns-73347.herokuapp.com/response?request_token=ds2UmHlddBqmj5CYRXafz0h42ov2w4ke&action=login&status=success
# https://safe-caverns-73347.herokuapp.com/response?request_token=Py1LeGTpDz4CYF84dweRKq1M5W23odGb&action=login&status=success

#access_token endpoint(params: request_token)
@app.route('/response', methods=["GET",'POST'])
def param():
	if request.method == 'GET':
		if request.args:
			if request.args.get('request_token', default=None, type=str) is not None and len(request.args['request_token']) != 0:
				token = request.args['request_token']
				print(token)
				try:
					host = "ec2-50-16-198-4.compute-1.amazonaws.com"
					database = "d4a38pnuog8ot6"
					user = "mgockdwzffwfoe"
					password = "0d797456c2dcd6c849832c99ee83243d13d68f3ca225eb622a949245ba8f9de9"
					pdb = psycopg2.connect(database=database, user=user, password=password, host=host, port="5432")
					check_broker = '''SELECT * FROM public."Broker" order by date desc'''
					result = pd.read_sql(check_broker, con=pdb)
					print(result)
					api_key = result.loc[0, 'api_key']
					api_secret = result.loc[0, 'api_secret']
					code = token
					kite = KiteConnect(api_key=api_key)
					data = kite.generate_session(code, api_secret)  
					print("data >> ", data)
					update_token = ''' UPDATE public."Broker" SET access_token='{}', date='{}' WHERE id={};  '''.format(data['access_token'], datetime.datetime.now(), result.loc[0, 'id'])
					print(update_token)
					c = pdb.cursor()
					result = c.execute(update_token)
					pdb.commit()
					result_json = {
						'login_status': 'succcess'
					}
					return jsonify(result_json)
				except Exception as e:
					print("error >> ", e)
					result_json = {
						'login_status': 'failed'
					}
					return jsonify(result_json)
				
			else:
				result_json = {
						'login_status': 'failed'
					}
				return jsonify(result_json)

		else:
			result_json = {
				'login_status': 'failed'
				}
			return jsonify(result_json)

	else:
		result_json = {
			'login_status': 'failed'
			}
		return jsonify(result_json)



if __name__ == '__main__':
	app.run(threaded=True)
