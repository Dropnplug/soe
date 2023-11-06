import flask as fl
from src.flask_src.app import app
from src.flask_src.deco import inspect_session

@app.route('/admin/logs/<path:path>', methods=['GET'])
@inspect_session(["admin"])
def logs(path):
	with open("./data/logs/"+path, "r") as f:
		content = f.read()
	return content.replace("\n", "<br>")