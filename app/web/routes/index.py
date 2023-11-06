import flask as fl
from src.flask_src.app import app

@app.route('/', methods=['GET'])
def index():
	return fl.render_template('index.html')