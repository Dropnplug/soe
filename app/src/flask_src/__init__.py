from .app import app
from .routes import import_routes
from .Flask_data import Flask_data
from src.memo import memo
import config

def fl_init():
	if "flask_data" not in memo.keys():
		memo["flask_data"] = Flask_data()
	app.secret_key = memo["flask_data"].get_key()
	import_routes()

def fl_run():
	app.run(host=config.FL_HOST, debug=config.FL_DEBUG, port=config.FL_PORT)