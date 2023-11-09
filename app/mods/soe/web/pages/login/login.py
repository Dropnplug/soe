import flask as fl
from src.flask_src.app import app

@app.route('/soe/login/', methods=['GET'])
def login_soe():
    return fl.render_template('/mods/soe/pages/login/login.html')

@app.route('/soe/logout/', methods=['GET'])
def logout_soe():
	fl.session.clear()
	return fl.redirect("/soe/")