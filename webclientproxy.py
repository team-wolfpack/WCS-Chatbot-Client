# ------------------------------------------------
# IMPORTS ----------------------------------------
# ------------------------------------------------
#####
# Python dist and 3rd party libraries
#####
import os, requests, json, string, datetime, logging, time

from os.path import join, dirname
from flask import Flask, request, render_template, redirect, url_for, Response, send_from_directory
# ------------------------------------------------
# FLASK ------------------------------------------
# ------------------------------------------------
app = Flask(__name__)


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logging.info("starting")
logging_comp_name = "STSA Web Client Proxy Main Loop"

CONVERSATION_URL = 'https://stsa-soe.mybluemix.net/v1/workspaces/voiceproxy/message'
if 'CONVERSATION_URL' in os.environ:
	CONVERSATION_URL = os.environ['CONVERSATION_URL']

CONVERSATION_USERNAME=''
if 'CONVERSATION_USERNAME' in os.environ:
	CONVERSATION_USERNAME = os.environ['CONVERSATION_USERNAME']


CONVERSATION_PASSWORD=''
if 'CONVERSATION_PASSWORD' in os.environ:
	CONVERSATION_PASSWORD = os.environ['CONVERSATION_PASSWORD']


#--------------- Web Test Client ----------------------------
@app.route('/webclient/')
def hello(name=None):
    return render_template('index.html', name=name)

@app.route('/js/<path:path>')
def send_js(path):
    return send_from_directory('static/js', path)
    
@app.route('/img/<path:path>')
def send_img(path):
    return send_from_directory('static/img', path)

@app.route('/css/<path:path>')
def send_css(path):
    return send_from_directory('static/css', path)

@app.route('/fonts/<path:path>')
def send_fonts(path):
    return send_from_directory('static/fonts', path)
    
@app.route('/api/message', methods=['POST'])
def restWebClientVoiceGatewayEntry():
	msg = json.loads(request.data)
	if 'context' not in msg:
		msg['context'] = {}
	
	resp_data = converse(msg)
	resp_data = json.dumps(resp_data, separators=(',',':'))
	return Response(resp_data, mimetype='application/json',status=200)

#-------------END Web Test Client------------------------


#------------ Time to talk to Node Red ------------------
def converse(message):
	POST_SUCCESS = 200
	r = requests.post(CONVERSATION_URL, auth=(CONVERSATION_USERNAME, CONVERSATION_PASSWORD), headers={'content-type': 'application/json'}, data=json.dumps(message))
	if r.status_code == POST_SUCCESS:
		message = r.json()
	
	return message

#--------------- Done with Node Red ---------------------

port = os.getenv('PORT', '5002')
if __name__ == "__main__":
	app.run(host='0.0.0.0', port=int(port))
	
