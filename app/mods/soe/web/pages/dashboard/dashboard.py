import flask as fl
from src.flask_src.app import app
from src.flask_src.deco import inspect_session
from mods.onduleur.src.utils import getLastDataFromBdd

@app.route('/soe/dashboard/', methods=['GET'])
@inspect_session([], redirect_url="/soe/logout/")
def dashboard_soe():
    return fl.render_template('/mods/soe/pages/dashboard/dashboard.html')

@app.route('/soe/dashboard/data/', methods=['GET'])
@inspect_session([], redirect_url="/soe/logout/")
def dashboard_data():
    return fl.jsonify(getLastDataFromBdd())