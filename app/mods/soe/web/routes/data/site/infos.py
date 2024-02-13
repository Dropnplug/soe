import flask as fl
from flask import request
from src.flask_src.app import app
from src.flask_src.deco import inspect_session
from mods.onduleur.src.utils import getLastDataFromBdd, getPmax, getOnduleursInfo, getDataFromBddInBetween, getDefauts, getDataFromBddInBetweenTstmp

@app.route('/soe/site/onduleursInfo/', methods=['GET'])
@inspect_session([], redirect_url="/soe/logout/")
def site_onduleur_info():
    return fl.jsonify(getOnduleursInfo())

@app.route('/soe/site/pMax/', methods=['GET'])
@inspect_session([], redirect_url="/soe/logout/")
def site_pmax():
    return fl.jsonify(getPmax())

@app.route('/soe/site/dataHisto/', methods=['POST'])
@inspect_session([], redirect_url="/soe/logout/")
def site_data_histo():
    params = request.get_json(force=True)
    return fl.jsonify(getDataFromBddInBetween(start=params["start"], end=params["end"]))

@app.route('/soe/site/getDataFromBdd/', methods=['POST'])
@inspect_session([], redirect_url="/soe/logout/")
def site_data_histo():
    params = request.get_json(force=True)
    return fl.jsonify(getDataFromBddInBetweenTstmp(start=params["start"], end=params["end"]))

@app.route('/soe/site/lastData/', methods=['GET'])
@inspect_session([], redirect_url="/soe/logout/")
def site_data():
    return fl.jsonify(getLastDataFromBdd())

@app.route('/soe/site/alarmes/', methods=['GET'])
@inspect_session([], redirect_url="/soe/logout/")
def onduleur_alarmes():
    return fl.jsonify(getDefauts())