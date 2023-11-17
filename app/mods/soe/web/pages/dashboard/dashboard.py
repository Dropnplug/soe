import flask as fl
from flask import request
from src.flask_src.app import app
from src.flask_src.deco import inspect_session
from mods.onduleur.src.utils import getLastDataFromBdd, getPmax, getOnduleursInfo, getDataFromBddInBetween

@app.route('/soe/dashboard/', methods=['GET'])
@inspect_session([], redirect_url="/soe/logout/")
def dashboard_soe():
    return fl.render_template('/mods/soe/pages/dashboard/dashboard.html')

@app.route('/soe/dashboard/data/', methods=['GET'])
@inspect_session([], redirect_url="/soe/logout/")
def dashboard_data():
    return fl.jsonify(getLastDataFromBdd())

@app.route('/soe/dashboard/dataHisto/', methods=['POST'])
@inspect_session([], redirect_url="/soe/logout/")
def dashboard_data_histo():
    params = request.get_json(force=True)
    return fl.jsonify(getDataFromBddInBetween(start=params["start"], end=params["end"]))

@app.route('/soe/dashboard/pMax/', methods=['GET'])
@inspect_session([], redirect_url="/soe/logout/")
def dashboard_pmax():
    return fl.jsonify(getPmax())

@app.route('/soe/dashboard/onduleursInfo/', methods=['GET'])
@inspect_session([], redirect_url="/soe/logout/")
def dashboard_onduleur_info():
    return fl.jsonify(getOnduleursInfo())