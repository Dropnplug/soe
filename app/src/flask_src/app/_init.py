import flask as fl
import os

TEMPLATE_DIR = './web/templates'
STATIC_DIR = './web/static'

def init():
	global app
	template_dir = os.path.abspath(TEMPLATE_DIR)
	static_dir = os.path.abspath(STATIC_DIR)
	app = fl.Flask(__name__, template_folder=template_dir, static_folder=static_dir)
	@app.after_request
	def prepare_response(response):
		response.headers.add("Access-Control-Allow-Origin", "*")
		return response
