import flask as fl
from src.flask_src.app import app
from src.flask_src.deco import inspect_session


@app.route('/admin/', methods=['GET'])
@inspect_session(["admin"])
def admin():
	return fl.render_template('admin/index.html')


@app.route('/admin/phpliteadmin/', methods=['GET'])
@inspect_session(["admin"])
def phpliteadmin():
	return fl.render_template('admin/phpliteadmin.html')