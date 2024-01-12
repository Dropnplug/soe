import flask as fl
from flask import request
from src.flask_src.app import app
from src.flask_src.deco import inspect_session

@app.route('/soe/alarmes/', methods=['GET'])
@inspect_session([], redirect_url="/soe/logout/")
def dashboard_soe():
    return fl.render_template('/mods/soe/pages/alarmes/alarmes.html')
